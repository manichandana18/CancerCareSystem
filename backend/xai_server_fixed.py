"""
Fixed Explainable AI Server - Port 8081
"""

import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from explainable_ai import ExplainableAI

# Create FastAPI app
app = FastAPI(title="Explainable AI Cancer Detection", version="2.0")

# Initialize XAI
xai = ExplainableAI()

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with XAI interface"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Explainable AI Cancer Detection</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .upload-area { border: 2px dashed #3498db; padding: 40px; text-align: center; margin: 20px 0; border-radius: 10px; background: #ecf0f1; cursor: pointer; }
            .upload-area:hover { background: #d5dbdb; }
            .result-section { margin: 20px 0; padding: 20px; border-radius: 10px; }
            .organ-result { background: #e8f5e8; border-left: 4px solid #27ae60; }
            .cancer-result { background: #fff3cd; border-left: 4px solid #f39c12; }
            .confidence-result { background: #d4edda; border-left: 4px solid #28a745; }
            .risk-result { background: #f8d7da; border-left: 4px solid #dc3545; }
            .explanation-box { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #007bff; }
            .medical-report { background: #e2e3e5; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .loading { display: none; text-align: center; color: #3498db; }
            .error { color: #e74c3c; background: #fadbd8; padding: 10px; border-radius: 5px; }
            .success { color: #27ae60; background: #d4efdf; padding: 10px; border-radius: 5px; }
            h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h3 { color: #34495e; margin-top: 20px; }
            .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .badge-high { background: #dc3545; color: white; }
            .badge-medium { background: #ffc107; color: black; }
            .badge-low { background: #28a745; color: white; }
            .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
            .status-online { background: #28a745; }
            .status-processing { background: #ffc107; animation: pulse 1.5s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Explainable AI Cancer Detection</h1>
                <p><span class="status-indicator status-online"></span>Medical-grade cancer detection with transparent AI reasoning</p>
            </div>
            
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <h3>📤 Upload Medical Image</h3>
                <p>Click to select or drag and drop a medical image (JPG, PNG, DICOM)</p>
                <input type="file" id="fileInput" accept="image/*" style="display: none;">
            </div>
            
            <div class="loading" id="loading">
                <h3><span class="status-indicator status-processing"></span>🔬 Analyzing with Explainable AI...</h3>
                <p>Please wait while our AI analyzes your medical image and generates explanations</p>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    uploadImage(file);
                }
            });
            
            // Drag and drop functionality
            const uploadArea = document.querySelector('.upload-area');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.background = '#d5dbdb';
            });
            
            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.style.background = '#ecf0f1';
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.background = '#ecf0f1';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadImage(files[0]);
                }
            });
            
            async function uploadImage(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                
                try {
                    const response = await fetch('/xai-predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('Server error: ' + response.status);
                    }
                    
                    const result = await response.json();
                    
                    if (result.error) {
                        throw new Error(result.error);
                    }
                    
                    displayResults(result);
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="error">❌ Error: ' + error.message + '</div>';
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            function displayResults(data) {
                let html = '';
                
                // Main Results
                html += '<div class="result-section organ-result">';
                html += '<h2>🎯 Organ Detection</h2>';
                html += '<p><strong>Detected Organ:</strong> ' + data.explanations.organ_detection.detected_organ.toUpperCase() + '</p>';
                html += '<p><strong>Confidence:</strong> ' + (data.explanations.organ_detection.confidence * 100).toFixed(1) + '%</p>';
                html += '<div class="explanation-box">';
                html += '<h4>AI Reasoning:</h4>';
                data.explanations.organ_detection.reasoning.forEach(reason => {
                    html += '<p>• ' + reason + '</p>';
                });
                html += '</div>';
                html += '</div>';
                
                // Cancer Detection
                html += '<div class="result-section cancer-result">';
                html += '<h2>🔬 Cancer Detection</h2>';
                html += '<p><strong>Diagnosis:</strong> ' + data.explanations.cancer_detection.diagnosis.toUpperCase() + '</p>';
                html += '<p><strong>Confidence:</strong> ' + data.explanations.cancer_detection.confidence + '%</p>';
                html += '<p><strong>Method:</strong> ' + data.explanations.cancer_detection.method + '</p>';
                html += '<div class="explanation-box">';
                html += '<h4>Cancer Indicators:</h4>';
                data.explanations.cancer_detection.cancer_indicators.forEach(indicator => {
                    html += '<p>• ' + indicator + '</p>';
                });
                html += '</div>';
                html += '</div>';
                
                // Confidence Analysis
                html += '<div class="result-section confidence-result">';
                html += '<h2>📊 Confidence Analysis</h2>';
                html += '<p><strong>Overall Confidence:</strong> ' + (data.explanations.confidence_analysis.overall_confidence * 100).toFixed(1) + '%</p>';
                html += '<p><strong>Reliability:</strong> ' + data.explanations.confidence_analysis.reliability_assessment.toUpperCase() + '</p>';
                html += '<div class="explanation-box">';
                html += '<h4>Confidence Factors:</h4>';
                data.explanations.confidence_analysis.confidence_factors.forEach(factor => {
                    html += '<p>• ' + factor + '</p>';
                });
                html += '</div>';
                html += '</div>';
                
                // Risk Assessment
                const riskLevel = data.explanations.risk_assessment.risk_level;
                const riskClass = riskLevel === 'high' ? 'badge-high' : riskLevel === 'medium' ? 'badge-medium' : 'badge-low';
                
                html += '<div class="result-section risk-result">';
                html += '<h2>⚠️ Risk Assessment</h2>';
                html += '<p><strong>Risk Level:</strong> <span class="badge ' + riskClass + '">' + riskLevel.toUpperCase() + '</span></p>';
                html += '<p><strong>Risk Score:</strong> ' + data.explanations.risk_assessment.risk_score.toFixed(1) + '</p>';
                html += '<div class="explanation-box">';
                html += '<h4>Contributing Factors:</h4>';
                data.explanations.risk_assessment.contributing_factors.forEach(factor => {
                    html += '<p>• ' + factor + '</p>';
                });
                html += '</div>';
                html += '</div>';
                
                // Medical Reasoning
                html += '<div class="result-section">';
                html += '<h2>🏥 Medical Reasoning</h2>';
                html += '<p><strong>Interpretation:</strong> ' + data.explanations.medical_reasoning.medical_interpretation + '</p>';
                html += '<p><strong>Clinical Significance:</strong> ' + data.explanations.medical_reasoning.clinical_significance + '</p>';
                html += '<div class="explanation-box">';
                html += '<h4>Recommended Actions:</h4>';
                data.explanations.medical_reasoning.recommended_actions.forEach(action => {
                    html += '<p>• ' + action + '</p>';
                });
                html += '</div>';
                html += '</div>';
                
                // Medical Report
                html += '<div class="medical-report">';
                html += '<h2>📋 Medical Report</h2>';
                html += '<p><strong>Report Type:</strong> ' + data.medical_report.report_type + '</p>';
                html += '<p><strong>Patient ID:</strong> ' + data.medical_report.patient_id + '</p>';
                html += '<p><strong>Exam Date:</strong> ' + new Date(data.medical_report.exam_date).toLocaleString() + '</p>';
                html += '<p><strong>Status:</strong> ' + data.medical_report.report_status.toUpperCase() + '</p>';
                html += '</div>';
                
                document.getElementById('results').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.post("/xai-predict")
async def xai_predict(file: UploadFile = File(...)):
    """XAI prediction endpoint"""
    
    try:
        # Read image
        image_bytes = await file.read()
        
        # Generate explanation
        explanation = xai.generate_explanation(image_bytes, filename_hint=file.filename)
        
        return explanation
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "Explainable AI is running", "version": "2.0", "port": 8081}

if __name__ == "__main__":
    print("🧠 Starting Explainable AI Server on Port 8081...")
    print("🌐 Open: http://127.0.0.1:8081")
    uvicorn.run(app, host="127.0.0.1", port=8081, reload=False)
