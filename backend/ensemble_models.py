#!/usr/bin/env python3
"""
Ensemble Models for Advanced Bone Cancer Detection
Multiple specialized models with different strengths
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import joblib
import os
from pathlib import Path

class BoneCancerEnsemble:
    """Advanced ensemble of multiple specialized models"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        self.ensemble = None
        self.is_trained = False
        
    def build_models(self):
        """Build individual specialized models"""
        
        # 1. XGBoost - Gradient Boosting (best for tabular data)
        self.models['xgboost'] = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='logloss'
        )
        
        # 2. LightGBM - Light Gradient Boosting (fast and efficient)
        self.models['lightgbm'] = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbose=-1
        )
        
        # 3. Random Forest - Classic ensemble (robust)
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        # 4. Neural Network - Deep Learning (captures complex patterns)
        self.models['neural_network'] = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=32,
            max_iter=500,
            random_state=42
        )
        
        # 5. SVM - Support Vector Machine (good for high-dimensional data)
        self.models['svm'] = SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            probability=True,
            random_state=42
        )
        
        # Create scalers for each model
        for name in self.models.keys():
            self.scalers[name] = StandardScaler()
        
        print("🚀 Built 5 specialized models:")
        print("   📊 XGBoost - Gradient Boosting")
        print("   💡 LightGBM - Light Gradient Boosting") 
        print("   🌲 Random Forest - Classic Ensemble")
        print("   🧠 Neural Network - Deep Learning")
        print("   🎯 SVM - Support Vector Machine")
    
    def train_ensemble(self, X, y):
        """Train all models and create voting ensemble"""
        print("🎯 Training Advanced Bone Cancer Ensemble...")
        
        # Split data for training
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train individual models
        trained_models = []
        model_names = []
        
        for name, model in self.models.items():
            print(f"   🔄 Training {name}...")
            
            # Scale features
            X_train_scaled = self.scalers[name].fit_transform(X_train)
            
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate on test set
            X_test_scaled = self.scalers[name].transform(X_test)
            accuracy = model.score(X_test_scaled, y_test)
            
            print(f"   ✅ {name}: {accuracy:.3f} accuracy")
            
            trained_models.append((name, model))
            model_names.append(name)
        
        # Create voting ensemble
        self.ensemble = VotingClassifier(
            estimators=trained_models,
            voting='soft',  # Use probabilities for better performance
            weights=[1.2, 1.1, 1.0, 1.1, 1.0]  # Give more weight to better models
        )
        
        # Train ensemble
        print("   🔄 Training voting ensemble...")
        X_train_ensemble = StandardScaler().fit_transform(X_train)
        self.ensemble.fit(X_train_ensemble, y_train)
        
        # Evaluate ensemble
        X_test_ensemble = StandardScaler().fit_transform(X_test)
        ensemble_accuracy = self.ensemble.score(X_test_ensemble, y_test)
        
        print(f"   🎉 Ensemble: {ensemble_accuracy:.3f} accuracy")
        print("🚀 Advanced Ensemble Training Complete!")
        
        self.is_trained = True
        self.feature_names = [f'feature_{i}' for i in range(X.shape[1])]
        
        return ensemble_accuracy
    
    def predict_proba(self, features):
        """Get prediction probabilities from ensemble"""
        if not self.is_trained:
            raise ValueError("Ensemble not trained yet!")
        
        # Scale features
        features_scaled = StandardScaler().fit_transform(features)
        
        # Get ensemble predictions
        probabilities = self.ensemble.predict_proba(features_scaled)
        
        return probabilities
    
    def predict(self, features):
        """Get predictions from ensemble"""
        if not self.is_trained:
            raise ValueError("Ensemble not trained yet!")
        
        # Scale features
        features_scaled = StandardScaler().fit_transform(features)
        
        # Get ensemble predictions
        predictions = self.ensemble.predict(features_scaled)
        probabilities = self.ensemble.predict_proba(features_scaled)
        
        return predictions, probabilities
    
    def get_feature_importance(self, model_name=None):
        """Get feature importance from individual models"""
        importance_dict = {}
        
        if model_name:
            # Get importance from specific model
            if model_name in self.models:
                model = self.models[model_name]
                if hasattr(model, 'feature_importances_'):
                    importance_dict[model_name] = model.feature_importances_
        else:
            # Get importance from all models that support it
            for name, model in self.models.items():
                if hasattr(model, 'feature_importances_'):
                    importance_dict[name] = model.feature_importances_
        
        return importance_dict
    
    def save_models(self, save_dir="models"):
        """Save all trained models"""
        if not self.is_trained:
            raise ValueError("No trained models to save!")
        
        save_path = Path(save_dir)
        save_path.mkdir(exist_ok=True)
        
        # Save individual models
        for name, model in self.models.items():
            model_path = save_path / f"bone_cancer_{name}.pkl"
            joblib.dump(model, model_path)
            
            # Save scaler
            scaler_path = save_path / f"bone_cancer_{name}_scaler.pkl"
            joblib.dump(self.scalers[name], scaler_path)
        
        # Save ensemble
        ensemble_path = save_path / "bone_cancer_ensemble.pkl"
        joblib.dump(self.ensemble, ensemble_path)
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'is_trained': self.is_trained,
            'model_count': len(self.models)
        }
        metadata_path = save_path / "bone_cancer_metadata.pkl"
        joblib.dump(metadata, metadata_path)
        
        print(f"💾 Saved all models to {save_path}")
    
    def load_models(self, load_dir="models"):
        """Load pre-trained models"""
        load_path = Path(load_dir)
        
        if not load_path.exists():
            raise FileNotFoundError(f"No models found in {load_dir}")
        
        # Load metadata
        metadata_path = load_path / "bone_cancer_metadata.pkl"
        if metadata_path.exists():
            metadata = joblib.load(metadata_path)
            self.feature_names = metadata['feature_names']
            self.is_trained = metadata['is_trained']
        
        # Load individual models
        for name in self.models.keys():
            model_path = load_path / f"bone_cancer_{name}.pkl"
            scaler_path = load_path / f"bone_cancer_{name}_scaler.pkl"
            
            if model_path.exists():
                self.models[name] = joblib.load(model_path)
                self.scalers[name] = joblib.load(scaler_path)
        
        # Load ensemble
        ensemble_path = load_path / "bone_cancer_ensemble.pkl"
        if ensemble_path.exists():
            self.ensemble = joblib.load(ensemble_path)
        
        print(f"📂 Loaded all models from {load_path}")

class EnsembleTrainer:
    """Helper class to train ensemble with radiomics features"""
    
    def __init__(self):
        self.ensemble = BoneCancerEnsemble()
        self.radiomics_extractor = None
        
    def prepare_training_data(self, image_paths, labels):
        """Prepare training data from images and labels"""
        from custom_radiomics import AdvancedRadiomicsExtractor
        
        self.radiomics_extractor = AdvancedRadiomicsExtractor()
        
        print("🔄 Extracting radiomics features...")
        features_list = []
        
        for i, image_path in enumerate(image_paths):
            try:
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
                
                features = self.radiomics_extractor.extract_all_features(image_bytes)
                features_list.append(list(features.values()))
                
                if (i + 1) % 10 == 0:
                    print(f"   Processed {i + 1}/{len(image_paths)} images")
                    
            except Exception as e:
                print(f"   ⚠️ Error processing {image_path}: {e}")
                continue
        
        X = np.array(features_list)
        y = np.array(labels)
        
        print(f"✅ Extracted {X.shape[1]} features from {len(features_list)} images")
        
        return X, y
    
    def train_and_save(self, image_paths, labels, save_dir="models"):
        """Complete training pipeline"""
        # Build models
        self.ensemble.build_models()
        
        # Prepare data
        X, y = self.prepare_training_data(image_paths, labels)
        
        # Train ensemble
        accuracy = self.ensemble.train_ensemble(X, y)
        
        # Save models
        self.ensemble.save_models(save_dir)
        
        return accuracy

# Test the ensemble system
if __name__ == "__main__":
    ensemble = BoneCancerEnsemble()
    ensemble.build_models()
    print("🎯 Advanced Bone Cancer Ensemble Ready!")
    print("🚀 5 specialized models built and ready for training!")
