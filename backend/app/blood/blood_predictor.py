from PIL import Image
import numpy as np
import io
import os
import sys
from pathlib import Path

# Add parent directory to path for importing Graph Neural Network
sys.path.append(str(Path(__file__).parent.parent.parent))

# Try to import Graph Neural Network
try:
    from graph_neural_network_blood import BloodCancerGNN
    GNN_AVAILABLE = True
except ImportError:
    GNN_AVAILABLE = False

# Lazy-load models
_gnn_model = None
CLASS_NAMES = ["normal", "leukemia"]

def _get_gnn_model():
    """Load Graph Neural Network model"""
    global _gnn_model
    if _gnn_model is not None:
        return _gnn_model
    try:
        if GNN_AVAILABLE:
            _gnn_model = BloodCancerGNN()
            # Try to load pre-trained GNN model
            model_path = Path(__file__).parent.parent.parent / "blood_gnn_model.h5"
            _gnn_model.load_pretrained_model(str(model_path) if model_path.exists() else None)
            print("Graph Neural Network loaded successfully")
            return _gnn_model
    except Exception as e:
        print(f"Graph Neural Network failed to load: {e}")
    return None

def predict_blood_cancer(image_bytes):
    """Predict blood cancer using Graph Neural Network"""
    
    # Try Graph Neural Network
    gnn_model = _get_gnn_model()
    if gnn_model is not None:
        try:
            result = gnn_model.predict_blood_cancer(image_bytes)
            result["method"] = "Graph Neural Network"
            result["model_type"] = "GNN-Blood"
            return result
        except Exception as e:
            print(f"Graph Neural Network prediction failed: {e}")
    
    # Ultimate fallback
    return {
        "diagnosis": "Error",
        "diagnosis_confidence": 0.0,
        "error": "Graph Neural Network not available",
        "method": "None"
    }

def get_blood_cell_analysis(image_bytes):
    """Get detailed blood cell analysis"""
    gnn_model = _get_gnn_model()
    if gnn_model is not None:
        try:
            # Preprocess to get cell information
            cell_features, adjacency, cells, original = gnn_model.preprocess_blood_image(image_bytes)
            
            return {
                "cell_count": len(cells),
                "cell_positions": [list(cell["position"]) for cell in cells],
                "cell_features": [cell["features"].tolist() for cell in cells],
                "graph_nodes": len(cells),
                "graph_edges": int(np.sum(adjacency > 0) / 2),
                "analysis_available": True
            }
        except Exception as e:
            return {"error": f"Cell analysis failed: {str(e)}", "analysis_available": False}
    else:
        return {"error": "Graph Neural Network not available", "analysis_available": False}
