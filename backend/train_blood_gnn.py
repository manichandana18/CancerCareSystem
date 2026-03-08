#!/usr/bin/env python3
"""
Train Graph Neural Network for Blood Cancer Detection
"""

import os
import numpy as np
import tensorflow as tf
from pathlib import Path
import json
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Import our GNN model
from graph_neural_network_blood import BloodCancerGNN

class BloodCancerTrainer:
    """Trainer for Blood Cancer Graph Neural Network"""
    
    def __init__(self, dataset_dir="blood_dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.train_dir = self.dataset_dir / "train"
        self.val_dir = self.dataset_dir / "val"
        self.test_dir = self.dataset_dir / "test"
        
        self.model = None
        self.class_names = ["normal", "leukemia"]
        self.class_to_idx = {name: idx for idx, name in enumerate(self.class_names)}
        
    def load_dataset(self, split_dir):
        """Load dataset from directory"""
        images = []
        labels = []
        
        for class_name in self.class_names:
            class_dir = split_dir / class_name
            if not class_dir.exists():
                continue
                
            for img_path in class_dir.glob("*.jpg"):
                try:
                    # Load image
                    with open(img_path, 'rb') as f:
                        image_bytes = f.read()
                    
                    images.append(image_bytes)
                    labels.append(self.class_to_idx[class_name])
                    
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
        
        return images, np.array(labels)
    
    def prepare_training_data(self, images, labels):
        """Prepare training data for GNN"""
        print("🔄 Preparing training data...")
        
        all_cell_features = []
        all_adjacency_matrices = []
        all_labels = []
        
        valid_samples = 0
        
        for i, (image_bytes, label) in enumerate(zip(images, labels)):
            try:
                # Create temporary GNN to process image
                temp_gnn = BloodCancerGNN()
                cell_features, adjacency, cells, _ = temp_gnn.preprocess_blood_image(image_bytes)
                
                # Only keep samples with enough cells
                if len(cells) >= 3:  # Need at least 3 cells for meaningful graph
                    all_cell_features.append(cell_features)
                    all_adjacency_matrices.append(adjacency)
                    all_labels.append(label)
                    valid_samples += 1
                else:
                    print(f"⚠️ Skipping sample {i}: only {len(cells)} cells detected")
                    
            except Exception as e:
                print(f"⚠️ Error processing sample {i}: {e}")
        
        print(f"✅ Prepared {valid_samples} valid samples")
        
        if valid_samples == 0:
            raise ValueError("No valid samples found")
        
        # Find maximum number of nodes
        max_nodes = max(features.shape[0] for features in all_cell_features)
        max_features = all_cell_features[0].shape[1]
        
        print(f"Max nodes: {max_nodes}, Features: {max_features}")
        
        # Pad all feature matrices to same size
        padded_features = []
        padded_adjacency = []
        
        for features, adj in zip(all_cell_features, all_adjacency_matrices):
            n_nodes = features.shape[0]
            
            # Pad features
            padded_feat = np.zeros((max_nodes, max_features))
            padded_feat[:n_nodes] = features
            padded_features.append(padded_feat)
            
            # Pad adjacency
            padded_adj = np.zeros((max_nodes, max_nodes))
            padded_adj[:n_nodes, :n_nodes] = adj
            padded_adjacency.append(padded_adj)
        
        return np.array(padded_features), np.array(padded_adjacency), np.array(all_labels)
    
    def create_model(self):
        """Create and compile GNN model"""
        print("🧠 Creating Graph Neural Network...")
        
        # Determine feature dimensions from sample data
        train_images, train_labels = self.load_dataset(self.train_dir)
        if len(train_images) == 0:
            raise ValueError("No training data found")
        
        # Get sample dimensions
        temp_gnn = BloodCancerGNN()
        sample_features, sample_adj, _, _ = temp_gnn.preprocess_blood_image(train_images[0])
        
        n_features = sample_features.shape[1]
        
        self.model = BloodCancerGNN(num_cell_features=n_features)
        self.model.load_pretrained_model()
        
        print(f"✅ Model created with {n_features} cell features")
    
    def train_model(self, epochs=50, batch_size=8):
        """Train the GNN model"""
        print("🚀 Starting training...")
        
        # Load datasets
        train_images, train_labels = self.load_dataset(self.train_dir)
        val_images, val_labels = self.load_dataset(self.val_dir)
        
        # Prepare data
        X_train_feat, X_train_adj, y_train = self.prepare_training_data(train_images, train_labels)
        X_val_feat, X_val_adj, y_val = self.prepare_training_data(val_images, val_labels)
        
        print(f"Training data shape: {X_train_feat.shape}, {X_train_adj.shape}")
        print(f"Validation data shape: {X_val_feat.shape}, {X_val_adj.shape}")
        
        # Create callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', patience=10, restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.5, patience=5
            )
        ]
        
        # Train model
        history = self.model.model.fit(
            [X_train_feat, X_train_adj], y_train,
            validation_data=([X_val_feat, X_val_adj], y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save training history
        self.save_training_history(history)
        
        return history
    
    def evaluate_model(self):
        """Evaluate the trained model"""
        print("📊 Evaluating model...")
        
        # Load test data
        test_images, test_labels = self.load_dataset(self.test_dir)
        X_test_feat, X_test_adj, y_test = self.prepare_training_data(test_images, test_labels)
        
        # Make predictions
        y_pred_proba = self.model.model.predict([X_test_feat, X_test_adj], verbose=0)
        y_pred = np.argmax(y_pred_proba, axis=1)
        
        # Calculate metrics
        report = classification_report(
            y_test, y_pred, 
            target_names=self.class_names,
            output_dict=True
        )
        
        cm = confusion_matrix(y_test, y_pred)
        
        # Print results
        print("\n📈 Classification Report:")
        for class_name in self.class_names:
            metrics = report[class_name]
            print(f"{class_name}:")
            print(f"  Precision: {metrics['precision']:.3f}")
            print(f"  Recall: {metrics['recall']:.3f}")
            print(f"  F1-Score: {metrics['f1-score']:.3f}")
        
        accuracy = report['accuracy']
        print(f"\n🎯 Overall Accuracy: {accuracy:.3f}")
        
        # Save results
        self.save_evaluation_results(report, cm)
        
        return report, cm
    
    def save_model(self, model_path="blood_gnn_model.h5"):
        """Save the trained model"""
        if self.model is not None:
            self.model.save_model(model_path)
            print(f"💾 Model saved to {model_path}")
    
    def save_training_history(self, history):
        """Save training history"""
        history_data = {
            'loss': [float(x) for x in history.history['loss']],
            'val_loss': [float(x) for x in history.history['val_loss']],
            'accuracy': [float(x) for x in history.history['accuracy']],
            'val_accuracy': [float(x) for x in history.history['val_accuracy']]
        }
        
        history_path = self.dataset_dir / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        print(f"📈 Training history saved to {history_path}")
    
    def save_evaluation_results(self, report, cm):
        """Save evaluation results"""
        results = {
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'class_names': self.class_names
        }
        
        results_path = self.dataset_dir / "evaluation_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Evaluation results saved to {results_path}")
    
    def plot_training_curves(self):
        """Plot training curves"""
        history_path = self.dataset_dir / "training_history.json"
        
        if not history_path.exists():
            print("No training history found")
            return
        
        with open(history_path, 'r') as f:
            history = json.load(f)
        
        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Loss plot
        ax1.plot(history['loss'], label='Training Loss')
        ax1.plot(history['val_loss'], label='Validation Loss')
        ax1.set_title('Model Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        
        # Accuracy plot
        ax2.plot(history['accuracy'], label='Training Accuracy')
        ax2.plot(history['val_accuracy'], label='Validation Accuracy')
        ax2.set_title('Model Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        
        plt.tight_layout()
        plot_path = self.dataset_dir / "training_curves.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Training curves saved to {plot_path}")
    
    def plot_confusion_matrix(self, cm):
        """Plot confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.class_names,
                   yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        plot_path = self.dataset_dir / "confusion_matrix.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Confusion matrix saved to {plot_path}")

def main():
    """Main training function"""
    print("🩸 Training Graph Neural Network for Blood Cancer Detection")
    print("=" * 60)
    
    # Check dataset exists
    dataset_dir = Path("blood_dataset")
    if not dataset_dir.exists():
        print("❌ Dataset not found. Run download_blood_dataset.py first")
        return
    
    # Create trainer
    trainer = BloodCancerTrainer()
    
    try:
        # Create model
        trainer.create_model()
        
        # Train model
        history = trainer.train_model(epochs=30, batch_size=4)
        
        # Evaluate model
        report, cm = trainer.evaluate_model()
        
        # Save model
        trainer.save_model()
        
        # Plot results
        trainer.plot_training_curves()
        trainer.plot_confusion_matrix(cm)
        
        print("\n✅ Training complete!")
        print(f"📁 Results saved to {dataset_dir}")
        print("🎯 Model ready for blood cancer detection!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
