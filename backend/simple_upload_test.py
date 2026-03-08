"""
Simple Upload Test - Fix image upload issues
"""

import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import io
from PIL import Image

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

# Create FastAPI app
app = FastAPI(title="Simple Upload Test", version="1.0")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Simple upload test interface"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Upload Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .upload-area { border: 3px dashed #3498db; padding: 40px; text-align: center; margin: 20px 0; border-radius: 10px; background: #ecf0f1; cursor: pointer; transition: all 0.3s; }
            .upload-area:hover { background: #d5dbdb; border-color: #2980b9; }
            .upload-area.dragover { background: #3498db; color: white; }
            .result { margin: 20px 0; padding: 20px; border-radius: 10px; background: #f8f9fa; }
            .success { background: #d4edda; border-left: 4px solid #28a745; }
            .error { background: #f8d7da; border-left: 4px solid #dc3545; }
            .loading { display: none; text-align: center; color: #3498db; }
            .file-info { background: #e2e3e5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            h1, h2 { color: #2c3e50; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .status-online { background: #d4edda; color: #155724; }
            .status-offline { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧪 Simple Upload Test</h1>
                <p>Test image upload functionality</p>
                <div id="serverStatus" class="status status-offline">🔴 Checking server status...</div>
            </div>
            
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <h3>📤 Click to Upload Image</h3>
                <p>Or drag and drop an image here</p>
                <input type="file" id="fileInput" accept="image/*" style="display: none;">
            </div>
            
            <div class="loading" id="loading">
                <h3>⏳ Processing...</h3>
                <p>Please wait while we analyze your image</p>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            // Check server status
            async function checkServerStatus() {
                try {
                    const response = await fetch('/health');
                    const data = await response.json();
                    document.getElementById('serverStatus').innerHTML = '🟢 Server is online: ' + data.status;
                    document.getElementById('serverStatus').className = 'status status-online';
                } catch (error) {
                    document.getElementById('serverStatus').innerHTML = '🔴 Server is offline: ' + error.message;
                    document.getElementById('serverStatus').className = 'status status-offline';
                }
            }
            
            // Check status on load
            checkServerStatus();
            setInterval(checkServerStatus, 5000);
            
            // File input handler
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    uploadFile(file);
                }
            });
            
            // Drag and drop handlers
            const uploadArea = document.querySelector('.upload-area');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadFile(files[0]);
                }
            });
            
            async function uploadFile(file) {
                console.log('Uploading file:', file.name);
                console.log('File size:', file.size, 'bytes');
                console.log('File type:', file.type);
                
                const formData = new FormData();
                formData.append('file', file);
                
                // Show file info
                let fileInfo = '<div class="file-info">';
                fileInfo += '<h4>📁 File Information:</h4>';
                fileInfo += '<p><strong>Name:</strong> ' + file.name + '</p>';
                fileInfo += '<p><strong>Size:</strong> ' + (file.size / 1024).toFixed(2) + ' KB</p>';
                fileInfo += '<p><strong>Type:</strong> ' + file.type + '</p>';
                fileInfo += '</div>';
                
                document.getElementById('results').innerHTML = fileInfo;
                document.getElementById('loading').style.display = 'block';
                
                try {
                    console.log('Sending request to /simple-upload...');
                    
                    const response = await fetch('/simple-upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    console.log('Response status:', response.status);
                    
                    if (!response.ok) {
                        throw new Error('HTTP ' + response.status + ': ' + response.statusText);
                    }
                    
                    const result = await response.json();
                    console.log('Response data:', result);
                    
                    displayResults(result);
                    
                } catch (error) {
                    console.error('Upload error:', error);
                    displayError(error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            function displayResults(data) {
                let html = '<div class="result success">';
                html += '<h2>✅ Upload Successful!</h2>';
                html += '<h3>🔬 Analysis Results:</h3>';
                html += '<p><strong>Organ:</strong> ' + (data.organ || 'Unknown') + '</p>';
                html += '<p><strong>Diagnosis:</strong> ' + (data.diagnosis || 'Unknown') + '</p>';
                html += '<p><strong>Confidence:</strong> ' + (data.confidence || '0') + '%</p>';
                
                if (data.debug) {
                    html += '<h4>🔍 Debug Info:</h4>';
                    html += '<pre>' + JSON.stringify(data.debug, null, 2) + '</pre>';
                }
                
                html += '</div>';
                
                document.getElementById('results').innerHTML = html;
            }
            
            function displayError(message) {
                let html = '<div class="result error">';
                html += '<h2>❌ Upload Failed</h2>';
                html += '<p><strong>Error:</strong> ' + message + '</p>';
                html += '<p>Please check your image and try again.</p>';
                html += '</div>';
                
                document.getElementById('results').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.post("/simple-upload")
async def simple_upload(file: UploadFile = File(...)):
    """Simple upload test endpoint"""
    
    try:
        print(f"📁 Received file: {file.filename}")
        print(f"📏 File size: {file.size}")
        print(f"📄 File type: {file.content_type}")
        
        # Read file content
        content = await file.read()
        print(f"📊 Content length: {len(content)} bytes")
        
        # Validate it's an image
        try:
            image = Image.open(io.BytesIO(content))
            print(f"🖼️ Image format: {image.format}")
            print(f"📐 Image size: {image.size}")
            image.verify()  # Verify it's a valid image
        except Exception as img_error:
            print(f"❌ Image validation error: {img_error}")
            return {"error": f"Invalid image file: {str(img_error)}"}
        
        # Process with auto_predict
        try:
            result = auto_predict(content, filename_hint=file.filename)
            
            response = {
                "success": True,
                "filename": file.filename,
                "organ": result.get('organ'),
                "diagnosis": result.get('diagnosis'),
                "confidence": result.get('diagnosis_confidence_pct'),
                "method": result.get('method'),
                "debug": {
                    "file_size": file.size,
                    "content_type": file.content_type,
                    "image_size": image.size if 'image' in locals() else None,
                    "full_result": result
                }
            }
            
            print("✅ Processing successful")
            return response
            
        except Exception as pred_error:
            print(f"❌ Prediction error: {pred_error}")
            return {"error": f"Prediction failed: {str(pred_error)}"}
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Upload failed: {str(e)}"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "Simple Upload Test is running", "version": "1.0"}

if __name__ == "__main__":
    print("🧪 Starting Simple Upload Test Server...")
    print("🌐 Open: http://127.0.0.1:8082")
    uvicorn.run(app, host="127.0.0.1", port=8082, reload=False)
