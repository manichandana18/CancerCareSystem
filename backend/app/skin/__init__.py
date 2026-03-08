"""
Skin Cancer Detection Module
Advanced AI-powered skin cancer detection with ABCD rule analysis
"""

from .skin_predictor import (
    predict_skin_cancer,
    extract_skin_features,
    specialized_skin_cancer_detector,
    get_skin_explainability
)

__all__ = [
    'predict_skin_cancer',
    'extract_skin_features',
    'specialized_skin_cancer_detector',
    'get_skin_explainability'
]
