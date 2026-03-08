"""
Mental Health Support Module for Cancer Patients
Comprehensive mental wellness and emotional support system
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import json
import random

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class MentalHealthSupport:
    """Comprehensive mental health support system for cancer patients"""
    
    def __init__(self):
        self.support_resources = {
            "anxiety_management": {
                "title": "Anxiety Management",
                "description": "Techniques to manage cancer-related anxiety",
                "techniques": [
                    "Deep breathing exercises",
                    "Progressive muscle relaxation",
                    "Mindfulness meditation",
                    "Guided imagery",
                    "Cognitive behavioral techniques"
                ],
                "resources": [
                    "5-4-3-2-1 Grounding Technique",
                    "Box Breathing (4-4-4-4)",
                    "Progressive Muscle Relaxation Script",
                    "Mindful Body Scan"
                ]
            },
            
            "depression_support": {
                "title": "Depression Support",
                "description": "Coping strategies for cancer-related depression",
                "techniques": [
                    "Behavioral activation",
                    "Positive psychology exercises",
                    "Social connection building",
                    "Goal setting and achievement",
                    "Gratitude practice"
                ],
                "resources": [
                    "Daily Mood Tracker",
                    "Gratitude Journal Template",
                    "Activity Scheduler",
                    "Positive Affirmations"
                ]
            },
            
            "stress_reduction": {
                "title": "Stress Reduction",
                "description": "Stress management techniques for cancer patients",
                "techniques": [
                    "Time management strategies",
                    "Relaxation techniques",
                    "Exercise and movement",
                    "Healthy sleep habits",
                    "Nutrition guidance"
                ],
                "resources": [
                    "Stress Assessment Tool",
                    "Sleep Hygiene Guide",
                    "Exercise Routine Planner",
                    "Nutrition Tips"
                ]
            },
            
            "emotional_support": {
                "title": "Emotional Support",
                "description": "Emotional wellness and coping strategies",
                "techniques": [
                    "Emotional regulation skills",
                    "Expressive writing",
                    "Art therapy techniques",
                    "Music therapy benefits",
                    "Peer support connections"
                ],
                "resources": [
                    "Emotion Regulation Worksheet",
                    "Journal Prompts for Cancer Patients",
                    "Art Therapy Ideas",
                    "Support Group Finder"
                ]
            },
            
            "family_support": {
                "title": "Family & Caregiver Support",
                "description": "Support for patients and their families",
                "techniques": [
                    "Family communication strategies",
                    "Caregiver self-care",
                    "Family meeting guidelines",
                    "Children's support resources",
                    "Partner relationship support"
                ],
                "resources": [
                    "Family Communication Guide",
                    "Caregiver Support Checklist",
                    "Children's Book Recommendations",
                    "Relationship Counseling Resources"
                ]
            }
        }
        
        self.daily_activities = {
            "morning": [
                "Morning meditation (5 minutes)",
                "Gratitude practice (3 things)",
                "Gentle stretching (10 minutes)",
                "Healthy breakfast planning"
            ],
            "afternoon": [
                "Mindful walking (15 minutes)",
                "Deep breathing breaks (2 minutes)",
                "Positive visualization",
                "Social connection call"
            ],
            "evening": [
                "Reflection journaling",
                "Progressive muscle relaxation",
                "Sleep preparation routine",
                "Tomorrow's positive intention"
            ]
        }
        
        self.emergency_resources = {
            "crisis_hotline": "988 (Suicide & Crisis Lifeline)",
            "cancer_support": "1-800-227-2345 (American Cancer Society)",
            "mental_health": "1-800-273-8255 (SAMHSA)",
            "emergency": "911 (Emergency Services)"
        }
    
    def get_personalized_support(self, patient_profile):
        """Get personalized mental health support based on patient profile"""
        
        support_plan = {
            "patient_id": patient_profile.get("id", "unknown"),
            "name": patient_profile.get("name", "Patient"),
            "cancer_type": patient_profile.get("cancer_type", "Unknown"),
            "treatment_stage": patient_profile.get("treatment_stage", "Unknown"),
            "support_recommendations": [],
            "daily_activities": [],
            "emergency_contacts": self.emergency_resources,
            "generated_at": datetime.now().isoformat()
        }
        
        # Personalize based on cancer type
        cancer_type = patient_profile.get("cancer_type", "").lower()
        if "lung" in cancer_type:
            support_plan["support_recommendations"].extend([
                "Breathing exercises tailored for lung cancer patients",
                "Anxiety management for breathing difficulties",
                "Support groups for lung cancer patients"
            ])
        elif "bone" in cancer_type:
            support_plan["support_recommendations"].extend([
                "Pain management mental strategies",
                "Mobility-focused emotional support",
                "Body image and self-esteem support"
            ])
        elif "brain" in cancer_type:
            support_plan["support_recommendations"].extend([
                "Cognitive function support",
                "Memory and focus exercises",
                "Neurological symptom coping"
            ])
        
        # Personalize based on treatment stage
        stage = patient_profile.get("treatment_stage", "").lower()
        if "diagnosis" in stage:
            support_plan["support_recommendations"].extend([
                "Shock and denial processing",
                "Decision-making support",
                "Information management strategies"
            ])
        elif "treatment" in stage:
            support_plan["support_recommendations"].extend([
                "Treatment side-effect coping",
                "Appointment anxiety management",
                "Hope and resilience building"
            ])
        elif "recovery" in stage or "remission" in stage:
            support_plan["support_recommendations"].extend([
                "Fear of recurrence management",
                "Return to normal life strategies",
                "Long-term survivorship support"
            ])
        
        # Add general support
        support_plan["support_recommendations"].extend([
            "Individual counseling recommendations",
            "Support group participation",
            "Family therapy options",
            "Stress management techniques"
        ])
        
        # Add daily activities
        support_plan["daily_activities"] = self.daily_activities
        
        return support_plan
    
    def get_crisis_support(self):
        """Get immediate crisis support resources"""
        
        return {
            "immediate_help": {
                "title": "Immediate Crisis Support",
                "hotlines": self.emergency_resources,
                "warning_signs": [
                    "Thoughts of self-harm",
                    "Extreme hopelessness",
                    "Inability to function",
                    "Severe panic attacks",
                    "Sudden mood changes"
                ],
                "immediate_actions": [
                    "Call 988 or 911 immediately",
                    "Go to nearest emergency room",
                    "Contact your treatment team",
                    "Don't wait - get help now"
                ]
            },
            "professional_help": {
                "title": "Professional Mental Health Support",
                "options": [
                    "Oncology social worker",
                    "Psychologist specializing in cancer",
                    "Psychiatrist for medication management",
                    "Counselor for talk therapy",
                    "Support group facilitator"
                ],
                "how_to_access": [
                    "Ask your oncology team for referral",
                    "Contact hospital patient services",
                    "Check with your insurance provider",
                    "Call mental health hotlines for referrals"
                ]
            }
        }
    
    def get_daily_inspiration(self):
        """Get daily inspirational message and activity"""
        
        inspirations = [
            "You are stronger than you think. Every day you face this with courage.",
            "Hope is the medicine that makes the burden of today lighter.",
            "Your journey is unique, and your strength is remarkable.",
            "Today is a new opportunity for healing and hope.",
            "You are not alone in this journey. We are here with you.",
            "Small victories count. Celebrate every moment of progress.",
            "Your resilience inspires others. You are a warrior.",
            "Tomorrow brings new possibilities and renewed strength."
        ]
        
        activities = [
            "Take 5 deep breaths and focus on the present moment",
            "Write down three things you're grateful for today",
            "Reach out to someone who supports you",
            "Do one small thing that brings you joy",
            "Practice self-compassion and kindness",
            "Visualize a peaceful, healing place",
            "Listen to calming music for 10 minutes",
            "Step outside and feel the sun on your face"
        ]
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "inspiration": random.choice(inspirations),
            "daily_activity": random.choice(activities),
            "motivational_quote": self.get_motivational_quote()
        }
    
    def get_motivational_quote(self):
        """Get motivational quote for cancer patients"""
        
        quotes = [
            "Cancer is a word, not a sentence. - John Diamond",
            "The human spirit is stronger than anything that happens to it. - C.C. Scott",
            "You beat cancer by how you live, why you live, and in the manner in which you live. - Stuart Scott",
            "There can be life after cancer. The prerequisite is early detection. - Katie Couric",
            "Cancer changes your life, often for the better. - Lance Armstrong",
            "When cancer happens, you don't put life on hold. You live now. - Fabiola Giatti"
        ]
        
        return random.choice(quotes)
    
    def get_support_groups(self):
        """Get information about support groups"""
        
        return {
            "online_support": {
                "title": "Online Support Groups",
                "options": [
                    "American Cancer Society Online Community",
                    "Cancer Support Community",
                    "Inspire (Cancer Support Groups)",
                    "Smart Patients (Cancer Forums)",
                    "Reddit r/cancer Support Community"
                ],
                "benefits": [
                    "24/7 access from home",
                    "Anonymous participation",
                    "Diverse patient experiences",
                    "Resource sharing"
                ]
            },
            "local_support": {
                "title": "Local Support Groups",
                "types": [
                    "Hospital-based support groups",
                    "Community cancer centers",
                    "American Cancer Society chapters",
                    "Gilda's Club locations",
                    "Cancer Support Community locations"
                ],
                "benefits": [
                    "Face-to-face connections",
                    "Local resource information",
                    "In-person activities",
                    "Professional facilitation"
                ]
            },
            "specialized_support": {
                "title": "Specialized Support Groups",
                "options": [
                    "Young adult cancer groups",
                    "Caregiver support groups",
                    "Family support groups",
                    "Bereavement support groups",
                    "Survivorship groups"
                ]
            }
        }

# Create FastAPI app for mental health support
app = FastAPI(title="Mental Health Support for Cancer Patients")

mental_health = MentalHealthSupport()

class PatientProfile(BaseModel):
    id: str
    name: str
    cancer_type: str
    treatment_stage: str
    age: int = None
    gender: str = None

@app.get("/", response_class=HTMLResponse)
async def mental_health_home():
    """Mental health support home page"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mental Health Support - CancerCare AI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px; 
            }
            .header { 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 30px; 
                margin-bottom: 20px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
            }
            .header h1 { 
                color: #2c3e50; 
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .header p { 
                color: #7f8c8d; 
                font-size: 1.2em;
            }
            .support-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
                margin-bottom: 20px; 
            }
            .support-card { 
                background: rgba(255,255,255,0.95); 
                border-radius: 15px; 
                padding: 25px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }
            .support-card:hover { 
                transform: translateY(-5px); 
            }
            .support-card h3 { 
                color: #3498db; 
                margin-bottom: 15px;
                font-size: 1.4em;
            }
            .support-card p { 
                color: #555; 
                line-height: 1.6;
                margin-bottom: 15px;
            }
            .techniques { 
                background: #ecf0f1; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 15px 0;
            }
            .techniques h4 { 
                color: #2c3e50; 
                margin-bottom: 10px;
            }
            .techniques ul { 
                margin: 0; 
                padding-left: 20px;
            }
            .techniques li { 
                margin: 5px 0; 
                color: #555;
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
            .daily-inspiration { 
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; 
                padding: 25px; 
                border-radius: 15px; 
                margin: 20px 0;
                text-align: center;
            }
            .daily-inspiration h3 { 
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .daily-inspiration p { 
                font-style: italic;
                font-size: 1.1em;
                margin: 10px 0;
            }
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
            .btn-success { 
                background: #27ae60; 
            }
            .btn-success:hover { 
                background: #229954; 
            }
            .btn-danger { 
                background: #e74c3c; 
            }
            .btn-danger:hover { 
                background: #c0392b; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Mental Health Support</h1>
                <p>Comprehensive emotional and psychological support for cancer patients</p>
            </div>
            
            <div class="daily-inspiration">
                <h3>💝 Daily Inspiration</h3>
                <p id="dailyMessage">Loading inspiration...</p>
                <p><strong>Today's Activity:</strong> <span id="dailyActivity">Loading...</span></p>
            </div>
            
            <div class="support-grid">
                <div class="support-card">
                    <h3>😰 Anxiety Management</h3>
                    <p>Techniques to manage cancer-related anxiety and panic attacks</p>
                    <div class="techniques">
                        <h4>Key Techniques:</h4>
                        <ul>
                            <li>Deep breathing exercises</li>
                            <li>Progressive muscle relaxation</li>
                            <li>Mindfulness meditation</li>
                            <li>Grounding techniques</li>
                        </ul>
                    </div>
                    <button class="btn" onclick="getSupportDetails('anxiety_management')">Learn More</button>
                </div>
                
                <div class="support-card">
                    <h3>😔 Depression Support</h3>
                    <p>Coping strategies for cancer-related depression and low mood</p>
                    <div class="techniques">
                        <h4>Key Techniques:</h4>
                        <ul>
                            <li>Behavioral activation</li>
                            <li>Positive psychology</li>
                            <li>Gratitude practice</li>
                            <li>Social connection</li>
                        </ul>
                    </div>
                    <button class="btn" onclick="getSupportDetails('depression_support')">Learn More</button>
                </div>
                
                <div class="support-card">
                    <h3>😰 Stress Reduction</h3>
                    <p>Stress management techniques specifically for cancer patients</p>
                    <div class="techniques">
                        <h4>Key Techniques:</h4>
                        <ul>
                            <li>Time management</li>
                            <li>Relaxation techniques</li>
                            <li>Exercise and movement</li>
                            <li>Sleep hygiene</li>
                        </ul>
                    </div>
                    <button class="btn" onclick="getSupportDetails('stress_reduction')">Learn More</button>
                </div>
                
                <div class="support-card">
                    <h3>💝 Emotional Support</h3>
                    <p>Emotional wellness and coping strategies for difficult emotions</p>
                    <div class="techniques">
                        <h4>Key Techniques:</h4>
                        <ul>
                            <li>Emotional regulation</li>
                            <li>Expressive writing</li>
                            <li>Art therapy</li>
                            <li>Peer support</li>
                        </ul>
                    </div>
                    <button class="btn" onclick="getSupportDetails('emotional_support')">Learn More</button>
                </div>
                
                <div class="support-card">
                    <h3>👨‍👩‍👧‍👦 Family Support</h3>
                    <p>Support for patients and their families/caregivers</p>
                    <div class="techniques">
                        <h4>Key Techniques:</h4>
                        <ul>
                            <li>Family communication</li>
                            <li>Caregiver self-care</li>
                            <li>Children's support</li>
                            <li>Partner support</li>
                        </ul>
                    </div>
                    <button class="btn" onclick="getSupportDetails('family_support')">Learn More</button>
                </div>
                
                <div class="support-card">
                    <h3>👥 Support Groups</h3>
                    <p>Connect with others who understand your journey</p>
                    <div class="techniques">
                        <h4>Available Options:</h4>
                        <ul>
                            <li>Online support communities</li>
                            <li>Local support groups</li>
                            <li>Specialized groups</li>
                            <li>Peer mentoring</li>
                        </ul>
                    </div>
                    <button class="btn btn-success" onclick="getSupportGroups()">Find Groups</button>
                </div>
            </div>
            
            <div class="emergency">
                <h3>🚨 Crisis Support</h3>
                <p>If you're in crisis, help is available 24/7</p>
                <p><strong>Crisis Hotline:</strong> 988</p>
                <p><strong>Cancer Support:</strong> 1-800-227-2345</p>
                <p><strong>Emergency:</strong> 911</p>
                <button class="btn btn-danger" onclick="getCrisisSupport()">Get Immediate Help</button>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h3>🧠 Get Personalized Support</h3>
                <p>Receive mental health recommendations tailored to your specific situation</p>
                <button class="btn btn-success" onclick="getPersonalizedSupport()">Get Personalized Plan</button>
            </div>
        </div>
        
        <script>
            // Load daily inspiration
            fetch('/daily-inspiration')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('dailyMessage').textContent = data.inspiration;
                    document.getElementById('dailyActivity').textContent = data.daily_activity;
                });
            
            function getSupportDetails(type) {
                fetch(`/support-details/${type}`)
                    .then(response => response.json())
                    .then(data => {
                        alert(data.title + '\\n\\n' + data.description + '\\n\\nTechniques:\\n' + data.techniques.join('\\n'));
                    });
            }
            
            function getSupportGroups() {
                fetch('/support-groups')
                    .then(response => response.json())
                    .then(data => {
                        let message = 'Support Groups Available:\\n\\n';
                        message += 'Online Support:\\n' + data.online_support.options.join('\\n') + '\\n\\n';
                        message += 'Local Support:\\n' + data.local_support.types.join('\\n');
                        alert(message);
                    });
            }
            
            function getCrisisSupport() {
                fetch('/crisis-support')
                    .then(response => response.json())
                    .then(data => {
                        let message = 'CRISIS SUPPORT:\\n\\n';
                        message += 'Hotlines:\\n';
                        for (const [key, value] of Object.entries(data.immediate_help.hotlines)) {
                            message += key + ': ' + value + '\\n';
                        }
                        message += '\\nWarning Signs:\\n' + data.immediate_help.warning_signs.join('\\n');
                        alert(message);
                    });
            }
            
            function getPersonalizedSupport() {
                const name = prompt('Enter your name:');
                const cancerType = prompt('Enter your cancer type (lung, bone, brain, etc.):');
                const treatmentStage = prompt('Enter your treatment stage (diagnosis, treatment, recovery):');
                
                if (name && cancerType && treatmentStage) {
                    fetch('/personalized-support', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            id: Date.now().toString(),
                            name: name,
                            cancer_type: cancerType,
                            treatment_stage: treatmentStage
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        let message = 'PERSONALIZED SUPPORT PLAN FOR ' + data.name.toUpperCase() + ':\\n\\n';
                        message += 'Cancer Type: ' + data.cancer_type + '\\n';
                        message += 'Treatment Stage: ' + data.treatment_stage + '\\n\\n';
                        message += 'Recommendations:\\n' + data.support_recommendations.join('\\n') + '\\n\\n';
                        message += 'Daily Activities:\\n' + data.daily_activities.morning.join('\\n') + '\\n';
                        alert(message);
                    });
                }
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/daily-inspiration")
async def get_daily_inspiration():
    """Get daily inspirational message"""
    return mental_health.get_daily_inspiration()

@app.get("/support-details/{support_type}")
async def get_support_details(support_type: str):
    """Get details for specific support type"""
    if support_type in mental_health.support_resources:
        return mental_health.support_resources[support_type]
    else:
        raise HTTPException(status_code=404, detail="Support type not found")

@app.get("/support-groups")
async def get_support_groups():
    """Get support group information"""
    return mental_health.get_support_groups()

@app.get("/crisis-support")
async def get_crisis_support():
    """Get crisis support resources"""
    return mental_health.get_crisis_support()

@app.post("/personalized-support")
async def get_personalized_support(profile: PatientProfile):
    """Get personalized mental health support"""
    return mental_health.get_personalized_support(profile.dict())

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "Mental Health Support Module Active", "version": "1.0"}

if __name__ == "__main__":
    print("🧠 STARTING MENTAL HEALTH SUPPORT MODULE")
    print("🌐 Open: http://127.0.0.1:8085")
    print("💝 Comprehensive mental wellness for cancer patients")
    print("=" * 60)
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8085, reload=False)
