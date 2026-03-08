import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

modules_to_test = [
    "fastapi",
    "uvicorn",
    "app.services.predictor",
    "app.lung.lung_predictor",
    "app.brain.brain_predictor",
    "app.services.explainability",
    "smart_organ_detector",
    "complete_blood_cancer",
    "skin_cancer_detector",
    "breast_cancer_detector",
    "confidence_enhancer",
    "normal_case_override",
    "differential_diagnosis",
    "app.services.auto_predict",
    "app.routes.auth",
    "app.routes.predict",
    "app.routes.auto_predict_route",
    "app.routes.blood_predict",
    "app.routes.brain_predict",
    "app.routes.skin_predict",
    "app.routes.breast_predict",
    "app.main"
]

print("🔍 Starting Import Diagnostic...")

for module_name in modules_to_test:
    try:
        print(f"🔄 Importing {module_name}...", end=" ", flush=True)
        __import__(module_name)
        print("✅ Success")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        traceback.print_exc()
    except BaseException as e:
        print(f"💀 CRITICAL FAILURE (BaseException): {e}")
        traceback.print_exc()
        sys.exit(1)

print("✨ Diagnostic Complete!")
