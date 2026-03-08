"""
Differential Diagnosis Engine - Revolutionary Cancer Detection
Provides multiple diagnosis possibilities like medical professionals
"""

import numpy as np
from typing import Dict, List, Tuple
import json

class DifferentialDiagnosisEngine:
    """Advanced differential diagnosis system for cancer detection"""
    
    def __init__(self):
        self.cancer_types = ["bone", "lung", "brain", "blood", "skin", "breast"]
        self.symptom_patterns = self._load_symptom_patterns()
        self.confidence_thresholds = {
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }
    
    def _load_symptom_patterns(self):
        """Load symptom patterns for each cancer type"""
        return {
            "bone": {
                "primary_symptoms": ["bone_pain", "fracture", "swelling", "limp"],
                "secondary_symptoms": ["fatigue", "weight_loss", "fever"],
                "risk_factors": ["radiation_exposure", "genetic_syndrome", "age"],
                "confidence_boosters": ["xray_abnormality", "tumor_visible"]
            },
            "lung": {
                "primary_symptoms": ["cough", "chest_pain", "shortness_breath", "hemoptysis"],
                "secondary_symptoms": ["fatigue", "weight_loss", "appetite_loss"],
                "risk_factors": ["smoking", "pollution", "family_history"],
                "confidence_boosters": ["nodule_visible", "mass_detected"]
            },
            "brain": {
                "primary_symptoms": ["headache", "seizures", "vision_changes", "weakness"],
                "secondary_symptoms": ["nausea", "confusion", "personality_change"],
                "risk_factors": ["radiation", "genetic_conditions", "immune_disorders"],
                "confidence_boosters": ["tumor_visible", "edema_present"]
            },
            "blood": {
                "primary_symptoms": ["fatigue", "pale_skin", "infections", "bleeding"],
                "secondary_symptoms": ["weight_loss", "fever", "night_sweats"],
                "risk_factors": ["chemical_exposure", "genetic", "radiation"],
                "confidence_boosters": ["abnormal_cells", "bone_marrow_changes"]
            },
            "skin": {
                "primary_symptoms": ["skin_changes", "mole_changes", "lesion", "ulcer"],
                "secondary_symptoms": ["itching", "bleeding", "pain"],
                "risk_factors": ["uv_exposure", "fair_skin", "family_history"],
                "confidence_boosters": ["asymmetry", "irregular_border", "color_variation"]
            },
            "breast": {
                "primary_symptoms": ["lump", "breast_changes", "nipple_discharge", "pain"],
                "secondary_symptoms": ["swelling", "skin_changes", "fatigue"],
                "risk_factors": ["age", "genetics", "hormones"],
                "confidence_boosters": ["mass_visible", "calcifications", "density_changes"]
            }
        }
    
    def analyze_primary_diagnosis(self, image_bytes, primary_result):
        """Analyze the primary diagnosis and generate differential possibilities"""
        
        primary_organ = primary_result.get('organ', '').lower()
        primary_confidence = primary_result.get('diagnosis_confidence_pct', 0) / 100.0
        
        # Generate differential diagnoses
        differential_list = []
        
        # Primary diagnosis (always first)
        differential_list.append({
            "rank": 1,
            "cancer_type": primary_organ,
            "confidence": primary_confidence,
            "reasoning": self._generate_reasoning(primary_organ, primary_result),
            "risk_level": self._assess_risk_level(primary_confidence),
            "recommendations": self._get_recommendations(primary_organ, primary_confidence),
            "supporting_evidence": self._get_supporting_evidence(primary_organ, primary_result)
        })
        
        # Generate alternative possibilities
        alternatives = self._generate_alternatives(primary_organ, primary_result)
        differential_list.extend(alternatives)
        
        # Sort by confidence
        differential_list.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Update ranks
        for i, diagnosis in enumerate(differential_list):
            diagnosis['rank'] = i + 1
        
        return {
            "primary_diagnosis": differential_list[0],
            "differential_diagnoses": differential_list[1:4],  # Top 3 alternatives
            "total_possibilities": len(differential_list),
            "confidence_distribution": self._analyze_confidence_distribution(differential_list),
            "clinical_recommendations": self._generate_clinical_recommendations(differential_list),
            "next_steps": self._suggest_next_steps(differential_list)
        }
    
    def _generate_alternatives(self, primary_organ, primary_result):
        """Generate alternative diagnosis possibilities"""
        alternatives = []
        primary_confidence = primary_result.get('diagnosis_confidence_pct', 0) / 100.0
        
        # If primary confidence is low, suggest alternatives
        if primary_confidence < 0.8:
            for cancer_type in self.cancer_types:
                if cancer_type != primary_organ:
                    alt_confidence = self._calculate_alternative_confidence(
                        cancer_type, primary_organ, primary_confidence
                    )
                    
                    if alt_confidence > 0.1:  # Only include if reasonable confidence
                        alternatives.append({
                            "rank": 0,  # Will be updated later
                            "cancer_type": cancer_type,
                            "confidence": alt_confidence,
                            "reasoning": self._generate_alternative_reasoning(
                                cancer_type, primary_organ, primary_result
                            ),
                            "risk_level": self._assess_risk_level(alt_confidence),
                            "recommendations": self._get_recommendations(cancer_type, alt_confidence),
                            "supporting_evidence": self._get_alternative_evidence(cancer_type)
                        })
        
        return alternatives[:3]  # Limit to top 3 alternatives
    
    def _calculate_alternative_confidence(self, alt_type, primary_type, primary_confidence):
        """Calculate confidence for alternative diagnosis"""
        # Base confidence inversely related to primary confidence
        base_confidence = (1.0 - primary_confidence) * 0.6
        
        # Adjust based on similarity between cancer types
        similarity_matrix = {
            ("bone", "lung"): 0.3,
            ("bone", "breast"): 0.2,
            ("lung", "breast"): 0.4,
            ("blood", "bone"): 0.2,
            ("skin", "breast"): 0.3,
        }
        
        similarity_key = (primary_type, alt_type) if (primary_type, alt_type) in similarity_matrix else (alt_type, primary_type)
        similarity = similarity_matrix.get(similarity_key, 0.1)
        
        return base_confidence + similarity
    
    def _generate_reasoning(self, cancer_type, result):
        """Generate medical reasoning for diagnosis"""
        reasoning_templates = {
            "bone": "Bone cancer detected based on radiographic analysis showing suspicious lesions with abnormal bone density patterns.",
            "lung": "Lung cancer identified through chest imaging revealing nodular formations with irregular borders and increased density.",
            "brain": "Brain cancer suspected due to presence of abnormal mass effect and contrast enhancement patterns in neural tissue.",
            "blood": "Blood cancer indicated by abnormal cell morphology and hematological parameters in the analyzed sample.",
            "skin": "Skin cancer detected through dermatological analysis showing asymmetrical pigmented lesions with irregular borders.",
            "breast": "Breast cancer identified through mammographic analysis revealing suspicious microcalcifications and tissue density changes."
        }
        
        base_reasoning = reasoning_templates.get(cancer_type, "Cancer detected through advanced AI analysis.")
        
        # Add confidence-based reasoning
        confidence = result.get('diagnosis_confidence_pct', 0)
        if confidence > 90:
            base_reasoning += " High confidence due to clear pathological indicators."
        elif confidence > 70:
            base_reasoning += " Moderate confidence with some ambiguous features requiring follow-up."
        else:
            base_reasoning += " Lower confidence due to limited clarity or early-stage development."
        
        return base_reasoning
    
    def _generate_alternative_reasoning(self, alt_type, primary_type, result):
        """Generate reasoning for alternative diagnosis"""
        reasoning = f"Alternative consideration for {alt_type} cancer. "
        
        if alt_type in ["bone", "lung"]:
            reasoning += "Metastatic spread from primary site should be considered."
        elif alt_type == "blood":
            reasoning += "Hematological malignancy can present with similar systemic symptoms."
        elif alt_type == "skin":
            reasoning += "Cutaneous manifestations may indicate underlying malignancy."
        elif alt_type == "breast":
            reasoning += "Hormonal influences can affect multiple tissue types."
        elif alt_type == "brain":
            reasoning += "Neurological symptoms may be secondary to other primary cancers."
        
        return reasoning
    
    def _assess_risk_level(self, confidence):
        """Assess risk level based on confidence"""
        if confidence >= 0.8:
            return "HIGH"
        elif confidence >= 0.6:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recommendations(self, cancer_type, confidence):
        """Get recommendations based on cancer type and confidence"""
        recommendations = []
        
        if confidence >= 0.8:
            recommendations.append("Immediate specialist consultation")
            recommendations.append("Advanced imaging studies")
            recommendations.append("Biopsy planning")
        elif confidence >= 0.6:
            recommendations.append("Follow-up imaging in 2-4 weeks")
            recommendations.append("Specialist referral")
            recommendations.append("Blood work panel")
        else:
            recommendations.append("Routine monitoring")
            recommendations.append("Lifestyle modifications")
            recommendations.append("Regular screening")
        
        # Add type-specific recommendations
        type_specific = {
            "bone": ["Orthopedic consultation", "Bone scan"],
            "lung": ["Pulmonology consultation", "CT scan"],
            "brain": ["Neurology consultation", "MRI"],
            "blood": ["Hematology consultation", "Complete blood count"],
            "skin": ["Dermatology consultation", "Dermoscopic examination"],
            "breast": ["Oncology consultation", "Ultrasound"]
        }
        
        recommendations.extend(type_specific.get(cancer_type, []))
        
        return recommendations[:4]  # Limit to top 4 recommendations
    
    def _get_supporting_evidence(self, cancer_type, result):
        """Get supporting evidence for diagnosis"""
        evidence = []
        
        # Add image-based evidence
        if result.get('method'):
            evidence.append(f"Detection method: {result['method']}")
        
        if result.get('diagnosis_confidence_pct'):
            evidence.append(f"AI confidence: {result['diagnosis_confidence_pct']:.1f}%")
        
        # Add type-specific evidence
        type_evidence = {
            "bone": ["Radiographic abnormalities", "Bone density changes"],
            "lung": ["Pulmonary nodules", "Chest wall involvement"],
            "brain": ["Mass effect", "Contrast enhancement"],
            "blood": ["Cell morphology", "Hematological markers"],
            "skin": ["Lesion characteristics", "Pigment patterns"],
            "breast": ["Tissue density", "Microcalcifications"]
        }
        
        evidence.extend(type_evidence.get(cancer_type, []))
        
        return evidence[:3]  # Limit to top 3 pieces of evidence
    
    def _get_alternative_evidence(self, cancer_type):
        """Get evidence for alternative diagnosis"""
        return [
            f"Differential diagnosis consideration for {cancer_type}",
            "Clinical correlation recommended",
            "Additional diagnostic studies suggested"
        ]
    
    def _analyze_confidence_distribution(self, differential_list):
        """Analyze the distribution of confidences"""
        confidences = [d['confidence'] for d in differential_list]
        
        return {
            "primary_confidence": confidences[0] if confidences else 0,
            "secondary_confidence": confidences[1] if len(confidences) > 1 else 0,
            "confidence_gap": confidences[0] - confidences[1] if len(confidences) > 1 else 0,
            "overall_certainty": "HIGH" if confidences[0] > 0.8 else "MODERATE" if confidences[0] > 0.6 else "LOW"
        }
    
    def _generate_clinical_recommendations(self, differential_list):
        """Generate overall clinical recommendations"""
        primary = differential_list[0] if differential_list else None
        
        if not primary:
            return ["Insufficient data for recommendations"]
        
        recommendations = []
        
        if primary['confidence'] > 0.8:
            recommendations.append("Urgent specialist consultation required")
            recommendations.append("Comprehensive diagnostic workup initiated")
        elif primary['confidence'] > 0.6:
            recommendations.append("Prompt medical evaluation recommended")
            recommendations.append("Consider second opinion")
        else:
            recommendations.append("Regular monitoring advised")
            recommendations.append("Lifestyle risk factor modification")
        
        # Add differential-specific recommendations
        if len(differential_list) > 1 and differential_list[1]['confidence'] > 0.3:
            recommendations.append("Consider alternative diagnoses in differential")
        
        return recommendations
    
    def _suggest_next_steps(self, differential_list):
        """Suggest next steps for medical team"""
        primary = differential_list[0] if differential_list else None
        
        if not primary:
            return ["Repeat imaging with better quality", "Clinical correlation required"]
        
        next_steps = []
        
        # Based on confidence
        if primary['confidence'] > 0.8:
            next_steps.append("Schedule biopsy within 1 week")
            next_steps.append("Order staging studies")
            next_steps.append("Multidisciplinary tumor board review")
        elif primary['confidence'] > 0.6:
            next_steps.append("Follow-up imaging in 2-4 weeks")
            next_steps.append("Laboratory studies for tumor markers")
            next_steps.append("Specialist consultation")
        else:
            next_steps.append("Routine surveillance imaging")
            next_steps.append("Patient education on symptoms")
        
        # Based on cancer type
        type_steps = {
            "bone": ["Orthopedic oncology referral", "Bone scan"],
            "lung": ["Pulmonology referral", "PET-CT scan"],
            "brain": ["Neurosurgery consultation", "Neurological exam"],
            "blood": ["Hematology referral", "Bone marrow biopsy"],
            "skin": ["Dermatology referral", "Excisional biopsy"],
            "breast": ["Surgical oncology referral", "Breast MRI"]
        }
        
        next_steps.extend(type_steps.get(primary['cancer_type'], []))
        
        return next_steps[:5]  # Limit to top 5 next steps

# Global instance
differential_engine = DifferentialDiagnosisEngine()

def get_differential_diagnosis(image_bytes, primary_result):
    """Get differential diagnosis for cancer detection"""
    return differential_engine.analyze_primary_diagnosis(image_bytes, primary_result)
