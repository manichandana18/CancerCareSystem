import base64
import io
import os

import numpy as np
from PIL import Image


def _as_float_confidence_0_1(confidence):
    if confidence is None:
        return None
    try:
        c = float(confidence)
    except Exception:
        return None
    return c / 100.0 if c > 1.0 else c


def explain_bone_radiomics(image_bytes, *, top_k=5):
    from app.services import predictor

    features_df = predictor.extract_features(image_bytes)

    importances = None
    if hasattr(predictor.bone_model, "feature_importances_"):
        importances = np.asarray(predictor.bone_model.feature_importances_, dtype=float)

    feature_names = list(features_df.columns)
    feature_values = features_df.iloc[0].to_dict()

    top_features = {}
    if importances is not None and len(importances) == len(feature_names):
        pairs = list(zip(feature_names, importances))
        pairs.sort(key=lambda x: x[1], reverse=True)
        for name, imp in pairs[:top_k]:
            top_features[name] = round(float(imp), 6)

    shap_details = None
    try:
        import shap  # type: ignore

        explainer = shap.TreeExplainer(predictor.bone_model)
        shap_values = explainer.shap_values(predictor.bone_scaler.transform(features_df))

        # Binary classifier: shap_values can be list[class] or array
        if isinstance(shap_values, list) and len(shap_values) >= 1:
            sv = shap_values[-1][0]
        else:
            sv = shap_values[0]

        shap_pairs = list(zip(feature_names, sv))
        shap_pairs.sort(key=lambda x: abs(float(x[1])), reverse=True)
        shap_top = {name: round(float(val), 6) for name, val in shap_pairs[:top_k]}
        shap_details = {"top_shap_values": shap_top}
    except Exception:
        shap_details = None

    return {
        "method": "Radiomics",
        "top_features": top_features,
        "feature_values": {k: round(float(v), 6) for k, v in feature_values.items()},
        "shap": shap_details,
    }


def _find_last_conv_layer_name(model):
    # Prefer last Conv2D-like layer
    for layer in reversed(model.layers):
        class_name = layer.__class__.__name__.lower()
        if "conv" in class_name and hasattr(layer, "output"):
            return layer.name
    return None


def explain_lung_gradcam(image_bytes, *, model_path=None):
    """Enhanced lung explainability with ViT attention + Grad-CAM fallback"""
    
    # Try Vision Transformer attention first
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent.parent))
        
        from app.lung.lung_predictor import get_lung_attention_visualization
        
        # Get attention visualization
        attention_result = get_lung_attention_visualization(image_bytes)
        
        if "error" not in attention_result:
            return {
                "method": "Vision Transformer Attention",
                "attention_maps": attention_result,
                "summary": "ViT attention shows model focus areas on lung nodules",
                "technology": "Multi-head self-attention"
            }
    except Exception as e:
        print(f"ViT attention failed: {e}")
    
    # Fallback to Grad-CAM
    try:
        import tensorflow as tf
    except Exception as e:
        return {"method": "Grad-CAM", "error": f"TensorFlow not available: {e}"}

    if model_path is None:
        # Use the trained lung model in backend root
        from pathlib import Path
        model_path = Path(__file__).parent.parent.parent / "lung_cancer_model.h5"
        if not model_path.exists():
            return {"method": "Grad-CAM", "error": f"Lung CNN model not found at {model_path}"}

    try:
        model = tf.keras.models.load_model(str(model_path))
    except Exception as e:
        return {"method": "Grad-CAM", "error": f"Failed to load lung model: {e}"}

    input_shape = model.input_shape
    if isinstance(input_shape, list):
        input_shape = input_shape[0]

    height = int(input_shape[1]) if len(input_shape) > 2 and input_shape[1] else 224
    width = int(input_shape[2]) if len(input_shape) > 2 and input_shape[2] else 224

    pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pil_resized = pil.resize((width, height))
    img = np.array(pil_resized).astype(np.float32) / 255.0
    inp = np.expand_dims(img, axis=0)

    last_conv = _find_last_conv_layer_name(model)
    if not last_conv:
        return {
            "method": "Grad-CAM",
            "error": "Could not find a convolution layer for Grad-CAM in the lung model.",
        }

    conv_layer = model.get_layer(last_conv)
    grad_model = tf.keras.models.Model([model.inputs], [conv_layer.output, model.output])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(inp)
        if predictions.shape[-1] == 1:
            class_channel = predictions[:, 0]
        else:
            class_idx = tf.argmax(predictions[0])
            class_channel = predictions[:, class_idx]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()

    # Convert heatmap to RGB overlay
    heatmap_uint8 = np.uint8(255 * heatmap)

    try:
        import cv2

        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        heatmap_color = cv2.resize(heatmap_color, (pil.size[0], pil.size[1]))

        original = np.array(pil).astype(np.uint8)
        overlay = np.clip(0.6 * original + 0.4 * heatmap_color, 0, 255).astype(np.uint8)
        out_pil = Image.fromarray(overlay)
    except Exception:
        # Fallback: return raw normalized heatmap only
        out_pil = Image.fromarray(np.uint8(255 * np.stack([heatmap] * 3, axis=-1)))

    buf = io.BytesIO()
    out_pil.save(buf, format="PNG")
    heatmap_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return {
        "method": "Grad-CAM",
        "heatmap_png_base64": heatmap_b64,
        "conv_layer": last_conv,
    }
