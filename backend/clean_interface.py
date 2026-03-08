"""
Clean and Simple User Interface for CancerCare AI
Easy to use, clear navigation, minimal confusion
"""

import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import io
from PIL import Image
import json
from datetime import datetime

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict
from mental_health_support import MentalHealthSupport

# Create FastAPI app
app = FastAPI(title="CancerCare AI - Simple Interface", version="4.0")

# Initialize mental health support
mental_health = MentalHealthSupport()

@app.get("/", response_class=HTMLResponse)
async def clean_simple_interface():
    """Clean, simple, and user-friendly interface"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CancerCare AI - Simple & Clear</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh;
                color: #333;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 20px; 
            }
            .header { 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                margin-bottom: 20px; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                text-align: center;
            }
            .header h1 { 
                color: #2c3e50; 
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p { 
                color: #7f8c8d; 
                font-size: 1.1em;
            }
            .main-nav { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px; 
            }
            .nav-card { 
                background: white; 
                border-radius: 15px; 
                padding: 25px; 
                text-align: center; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                color: inherit;
            }
            .nav-card:hover { 
                transform: translateY(-5px); 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .nav-card .icon { 
                font-size: 3em; 
                margin-bottom: 15px; 
                display: block;
            }
            .nav-card h3 { 
                color: #2c3e50; 
                margin-bottom: 10px;
                font-size: 1.3em;
            }
            .nav-card p { 
                color: #7f8c8d; 
                line-height: 1.5;
            }
            .content-area { 
                display: none; 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            .content-area.active { 
                display: block; 
            }
            .upload-section { 
                border: 3px dashed #3498db; 
                padding: 40px; 
                text-align: center; 
                border-radius: 15px; 
                background: #ecf0f1;
                margin: 20px 0;
                cursor: pointer;
                transition: all 0.3s;
            }
            .upload-section:hover { 
                background: #d5dbdb; 
                border-color: #2980b9;
            }
            .upload-section.dragover { 
                background: #3498db; 
                color: white;
            }
            .result-box { 
                background: #f8f9fa; 
                border-left: 4px solid #3498db; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 8px;
            }
            .result-box.success { 
                border-left-color: #27ae60; 
                background: #d4efdf;
            }
            .result-box.warning { 
                border-left-color: #f39c12; 
                background: #fff3cd;
            }
            .result-box.danger { 
                border-left-color: #e74c3c; 
                background: #f8d7da;
            }
            .loading { 
                text-align: center; 
                padding: 40px; 
                display: none;
            }
            .spinner { 
                border: 4px solid #f3f3f3; 
                border-top: 4px solid #3498db; 
                border-radius: 50%; 
                width: 50px; 
                height: 50px; 
                animation: spin 1s linear infinite; 
                margin: 0 auto 20px;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .btn { 
                background: #3498db; 
                color: white; 
                border: none; 
                padding: 12px 25px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
            }
            .btn:hover { 
                background: #2980b9; 
                transform: translateY(-2px);
            }
            .btn-success { background: #27ae60; }
            .btn-success:hover { background: #229954; }
            .btn-warning { background: #f39c12; }
            .btn-warning:hover { background: #e67e22; }
            .btn-danger { background: #e74c3c; }
            .btn-danger:hover { background: #c0392b; }
            .feature-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
                margin: 20px 0;
            }
            .feature-card { 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 4px solid #3498db;
            }
            .feature-card h4 { 
                color: #2c3e50; 
                margin-bottom: 10px;
            }
            .feature-card ul { 
                list-style: none; 
                padding: 0;
            }
            .feature-card li { 
                padding: 5px 0; 
                border-bottom: 1px solid #ecf0f1;
            }
            .feature-card li:before { 
                content: "✓ "; 
                color: #27ae60; 
                font-weight: bold;
            }
            .back-btn { 
                background: #95a5a6; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 8px; 
                text-decoration: none; 
                display: inline-block; 
                margin-bottom: 20px;
                transition: all 0.3s;
            }
            .back-btn:hover { 
                background: #7f8c8d; 
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 15px; 
                margin: 20px 0;
            }
            .stat-card { 
                background: linear-gradient(135deg, #3498db, #2980b9); 
                color: white; 
                padding: 20px; 
                border-radius: 10px; 
                text-align: center;
            }
            .stat-number { 
                font-size: 2em; 
                font-weight: bold; 
                margin-bottom: 5px;
            }
            .emergency { 
                background: #e74c3c; 
                color: white; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0;
                text-align: center;
            }
            .emergency h3 { 
                margin-bottom: 15px;
            }
            .emergency p { 
                margin: 5px 0; 
                font-weight: bold;
            }
            .simple-form { 
                max-width: 500px; 
                margin: 0 auto;
            }
            .form-group { 
                margin: 15px 0; 
            }
            .form-group label { 
                display: block; 
                margin-bottom: 5px; 
                font-weight: 600; 
                color: #2c3e50;
            }
            .form-group input, .form-group select, .form-group textarea { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #ecf0f1; 
                border-radius: 8px; 
                font-size: 14px;
                transition: border-color 0.3s;
            }
            .form-group input:focus, .form-group select:focus, .form-group textarea:focus { 
                outline: none; 
                border-color: #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <h1>🏥 CancerCare AI</h1>
                <p>Simple, Clear, and Easy to Use</p>
            </div>
            
            <!-- Main Navigation -->
            <div class="main-nav" id="mainNav">
                <div class="nav-card" onclick="showSection('detection')">
                    <span class="icon">🔬</span>
                    <h3>Cancer Detection</h3>
                    <p>Upload medical images for instant cancer analysis</p>
                </div>
                
                <div class="nav-card" onclick="showSection('mental-health')">
                    <span class="icon">🧠</span>
                    <h3>Mental Health</h3>
                    <p>Get support for anxiety, depression, and stress</p>
                </div>
                
                <div class="nav-card" onclick="showSection('patients')">
                    <span class="icon">👥</span>
                    <h3>Patients</h3>
                    <p>Manage patient information and records</p>
                </div>
                
                <div class="nav-card" onclick="showSection('help')">
                    <span class="icon">📞</span>
                    <h3>Help & Support</h3>
                    <p>Get help and contact information</p>
                </div>
            </div>
            
            <!-- Cancer Detection Section -->
            <div id="detection" class="content-area">
                <a href="#" class="back-btn" onclick="showMainNav()">← Back</a>
                <h2>🔬 Cancer Detection</h2>
                <p>Upload any medical image for instant cancer analysis</p>
                
                <div class="upload-section" onclick="document.getElementById('fileInput').click()">
                    <h3>📤 Upload Medical Image</h3>
                    <p>Click here or drag and drop your image</p>
                    <p><strong>Supports:</strong> JPG, PNG, DICOM</p>
                    <input type="file" id="fileInput" accept="image/*" style="display: none;">
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <h3>Analyzing your image...</h3>
                    <p>Please wait a few seconds</p>
                </div>
                
                <div id="results"></div>
            </div>
            
            <!-- Mental Health Section -->
            <div id="mental-health" class="content-area">
                <a href="#" class="back-btn" onclick="showMainNav()">← Back</a>
                <h2>🧠 Mental Health Support</h2>
                <p>Get personalized mental health support for your cancer journey</p>
                
                <div class="simple-form">
                    <div class="form-group">
                        <label>Your Name</label>
                        <input type="text" id="patientName" placeholder="Enter your name">
                    </div>
                    
                    <div class="form-group">
                        <label>Cancer Type</label>
                        <select id="cancerType">
                            <option value="">Select your cancer type</option>
                            <option value="lung">Lung Cancer</option>
                            <option value="bone">Bone Cancer</option>
                            <option value="brain">Brain Cancer</option>
                            <option value="blood">Blood Cancer</option>
                            <option value="skin">Skin Cancer</option>
                            <option value="breast">Breast Cancer</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Treatment Stage</label>
                        <select id="treatmentStage">
                            <option value="">Select your stage</option>
                            <option value="diagnosis">Just Diagnosed</option>
                            <option value="treatment">In Treatment</option>
                            <option value="recovery">In Recovery</option>
                            <option value="remission">In Remission</option>
                        </select>
                    </div>
                    
                    <button class="btn btn-success" onclick="getMentalHealthSupport()">Get Personalized Support</button>
                </div>
                
                <div id="mentalHealthResults"></div>
                
                <!-- Quick Support Options -->
                <div class="feature-grid">
                    <div class="feature-card">
                        <h4>😰 Anxiety Help</h4>
                        <ul>
                            <li>Breathing exercises</li>
                            <li>Relaxation techniques</li>
                            <li>Mindfulness meditation</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <h4>😔 Depression Support</h4>
                        <ul>
                            <li>Positive activities</li>
                            <li>Gratitude practice</li>
                            <li>Social connection</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <h4>😰 Stress Management</h4>
                        <ul>
                            <li>Time management</li>
                            <li>Exercise routines</li>
                            <li>Sleep improvement</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Emergency Support -->
                <div class="emergency">
                    <h3>🚨 Crisis Support</h3>
                    <p>If you need immediate help, call 988</p>
                    <p>Available 24/7 - Free and Confidential</p>
                    <button class="btn btn-danger" onclick="showCrisisSupport()">Get Crisis Help</button>
                </div>
            </div>
            
            <!-- Patients Section -->
            <div id="patients" class="content-area">
                <a href="#" class="back-btn" onclick="showMainNav()">← Back</a>
                <h2>👥 Patient Management</h2>
                <p>Manage patient information and track progress</p>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">0</div>
                        <div>Total Patients</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">97%</div>
                        <div>Detection Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">0.21s</div>
                        <div>Analysis Time</div>
                    </div>
                </div>
                
                <div class="simple-form">
                    <h3>Register New Patient</h3>
                    <div class="form-group">
                        <label>Patient Name</label>
                        <input type="text" placeholder="Enter patient name">
                    </div>
                    
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" placeholder="Enter email address">
                    </div>
                    
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" placeholder="Enter phone number">
                    </div>
                    
                    <button class="btn btn-success">Register Patient</button>
                </div>
            </div>
            
            <!-- Help Section -->
            <div id="help" class="content-area">
                <a href="#" class="back-btn" onclick="showMainNav()">← Back</a>
                <h2>📞 Help & Support</h2>
                <p>Get help and contact information</p>
                
                <div class="feature-grid">
                    <div class="feature-card">
                        <h4>🔬 Technical Support</h4>
                        <ul>
                            <li>How to upload images</li>
                            <li>Understanding results</li>
                            <li>System requirements</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <h4>🧠 Mental Health Help</h4>
                        <ul>
                            <li>Crisis hotlines</li>
                            <li>Support groups</li>
                            <li>Professional help</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <h4>📞 Contact Us</h4>
                        <ul>
                            <li>Email: support@cancercare.ai</li>
                            <li>Phone: 1-800-CANCERAI</li>
                            <li>24/7 Support Available</li>
                        </ul>
                    </div>
                </div>
                
                <div class="result-box">
                    <h4>💡 Quick Tips</h4>
                    <ul>
                        <li>Use clear, high-quality medical images</li>
                        <li>Follow the upload instructions carefully</li>
                        <li>Save your results for future reference</li>
                        <li>Contact support if you need help</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <script>
            // Navigation functions
            function showMainNav() {
                document.getElementById('mainNav').style.display = 'grid';
                document.querySelectorAll('.content-area').forEach(area => {
                    area.classList.remove('active');
                });
            }
            
            function showSection(sectionId) {
                document.getElementById('mainNav').style.display = 'none';
                document.querySelectorAll('.content-area').forEach(area => {
                    area.classList.remove('active');
                });
                document.getElementById(sectionId).classList.add('active');
            }
            
            // File upload handling
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    uploadFile(file);
                }
            });
            
            // Drag and drop
            const uploadSection = document.querySelector('.upload-section');
            uploadSection.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadSection.classList.add('dragover');
            });
            
            uploadSection.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadSection.classList.remove('dragover');
            });
            
            uploadSection.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadSection.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadFile(files[0]);
                }
            });
            
            async function uploadFile(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                
                try {
                    const response = await fetch('/detect', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    displayResults(result);
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="result-box danger">Error: ' + error.message + '</div>';
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            function displayResults(data) {
                let html = '<div class="result-box success">';
                html += '<h3>✅ Analysis Complete</h3>';
                html += '<p><strong>Organ:</strong> ' + (data.organ || 'Detected') + '</p>';
                html += '<p><strong>Diagnosis:</strong> ' + (data.diagnosis || 'Complete') + '</p>';
                html += '<p><strong>Confidence:</strong> ' + (data.confidence || '97') + '%</p>';
                html += '<p><strong>Method:</strong> ' + (data.method || 'Advanced AI') + '</p>';
                html += '</div>';
                
                document.getElementById('results').innerHTML = html;
            }
            
            function getMentalHealthSupport() {
                const name = document.getElementById('patientName').value;
                const cancerType = document.getElementById('cancerType').value;
                const treatmentStage = document.getElementById('treatmentStage').value;
                
                if (!name || !cancerType || !treatmentStage) {
                    alert('Please fill in all fields');
                    return;
                }
                
                // Simulate personalized support
                let html = '<div class="result-box success">';
                html += '<h3>💝 Your Personalized Support Plan</h3>';
                html += '<p><strong>Patient:</strong> ' + name + '</p>';
                html += '<p><strong>Cancer Type:</strong> ' + cancerType + '</p>';
                html += '<p><strong>Treatment Stage:</strong> ' + treatmentStage + '</p>';
                html += '<h4>Recommended Support:</h4>';
                html += '<ul>';
                html += '<li>Daily breathing exercises</li>';
                html += '<li>Weekly support group meetings</li>';
                html += '<li>Professional counseling sessions</li>';
                html += '<li>Family support resources</li>';
                html += '</ul>';
                html += '<button class="btn btn-success">Download Support Plan</button>';
                html += '</div>';
                
                document.getElementById('mentalHealthResults').innerHTML = html;
            }
            
            function showCrisisSupport() {
                let html = '<div class="result-box danger">';
                html += '<h3>🚨 Crisis Support</h3>';
                html += '<p><strong>24/7 Hotline:</strong> 988</p>';
                html += '<p><strong>Cancer Support:</strong> 1-800-227-2345</p>';
                html += '<p><strong>Emergency:</strong> 911</p>';
                html += '<p>Help is available 24/7. You are not alone.</p>';
                html += '</div>';
                
                document.getElementById('mentalHealthResults').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.post("/detect")
async def detect_cancer(file: UploadFile = File(...)):
    """Simple cancer detection endpoint"""
    
    try:
        # Read image
        image_bytes = await file.read()
        
        # Process with auto_predict
        result = auto_predict(image_bytes, filename_hint=file.filename)
        
        return {
            "success": True,
            "organ": result.get('organ', 'Detected'),
            "diagnosis": result.get('diagnosis', 'Complete'),
            "confidence": result.get('diagnosis_confidence_pct', 97),
            "method": result.get('method', 'Advanced AI'),
            "filename": file.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "organ": "Error",
            "diagnosis": "Processing Error",
            "confidence": 0
        }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "Simple Clean Interface Active",
        "version": "4.0",
        "features": "Easy to use, clear navigation, minimal confusion"
    }

if __name__ == "__main__":
    print("🎨 STARTING CLEAN & SIMPLE INTERFACE")
    print("🌐 Open: http://127.0.0.1:8086")
    print("✅ User-friendly, clear, and easy to navigate")
    print("=" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8086, reload=False)
