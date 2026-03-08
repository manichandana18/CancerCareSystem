import traceback
import sys
import os

try:
    print("STARTING CancerCare Backend Diagnostic Runner")
    # Add the current directory to sys.path to resolve 'app' module
    sys.path.append(os.getcwd())
    
    from app.main import app
    import uvicorn
    
    print("LOG: App imported successfully")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
except Exception as e:
    print("CRITICAL ERROR DURING STARTUP:")
    traceback.print_exc()
    sys.exit(1)
