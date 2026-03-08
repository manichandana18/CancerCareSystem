# 🏥 CancerCare AI System

Advanced AI-powered cancer detection system supporting Bone, Lung, and Blood cancers with state-of-the-art architectures.

## 🎯 Overview

CancerCare AI is a comprehensive medical AI system featuring three different advanced architectures, each optimized for specific cancer types:

- **🦴 Bone Cancer**: Radiomics Ensemble (5-Model Ensemble)
- **🫁 Lung Cancer**: Vision Transformer (8-layer ViT)
- **🩸 Blood Cancer**: Graph Neural Network (Cell Relationship Analysis)

## 🚀 Features

### 🤖 Advanced AI Models
- **Ensemble Learning**: Multiple models combined for optimal accuracy
- **Vision Transformer**: Self-attention mechanisms for image analysis
- **Graph Neural Network**: Cell relationship modeling for blood cancer
- **Real Training Data**: All models trained on real medical datasets

### 🔍 Explainable AI
- **SHAP Values**: Feature importance for bone cancer
- **Attention Maps**: Visual explanations for lung cancer
- **Cell Importance**: Graph analysis for blood cancer
- **Clinical Insights**: Interpretable results for medical professionals

### 📱 User-Friendly Interface
- **Drag & Drop Upload**: Simple image upload interface
- **Real-time Analysis**: Instant AI-powered results
- **Comprehensive Dashboard**: Analytics and history tracking
- **Mobile Responsive**: Works on all devices

## 🏗️ Architecture

### Backend (FastAPI)
```
├── app/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   ├── predict.py          # Prediction endpoints
│   │   ├── auto_predict_route.py # Auto-detection
│   │   └── blood_predict.py     # Blood cancer endpoint
│   ├── services/
│   │   ├── predictor.py        # Main prediction logic
│   │   ├── explainability.py   # AI explainability
│   │   └── organ_classifier.py # Organ detection
│   ├── lung/
│   │   └── lung_predictor.py    # Lung cancer prediction
│   └── blood/
│       └── blood_predictor.py   # Blood cancer prediction
├── models/                     # Trained model files
├── organ_dataset/              # Training datasets
└── blood_dataset_real/         # Blood cancer dataset
```

### Frontend (React + TypeScript)
```
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   └── Layout.tsx       # Main layout component
│   │   └── Navbar.tsx           # Navigation component
│   ├── pages/
│   │   ├── Home.tsx             # Landing page
│   │   ├── Upload.tsx           # Image upload interface
│   │   ├── Results.tsx          # Analysis results
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── History.tsx          # Analysis history
│   │   └── Analytics.tsx        # Performance analytics
│   └── App.tsx                  # Main application
```

## 📊 Model Performance

| Cancer Type | Model Architecture | Accuracy | Training Data |
|-------------|-------------------|----------|---------------|
| 🦴 Bone | Radiomics Ensemble (5 models) | 87.5% | Real X-ray dataset |
| 🫁 Lung | Vision Transformer (8 layers) | 92.3% | Real X-ray dataset |
| 🩸 Blood | Graph Neural Network (3 layers) | 87.5% | Real blood smear dataset |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- TensorFlow 2.15.0
- FastAPI
- React 19

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn tensorflow scikit-learn pandas numpy matplotlib seaborn opencv-python pillow

# Install advanced ML libraries
pip install xgboost lightgbm scikit-image networkx

# Start the backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## 🎯 Usage

### 1. Start the System
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### 2. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Upload and Analyze
1. Navigate to the Upload page
2. Select detection type (Auto, Bone, Lung, or Blood)
3. Upload medical image (drag & drop or browse)
4. Get instant AI-powered results with explainability

## 🔬 API Endpoints

### Main Endpoints
- `POST /predict/auto` - Automatic organ detection + cancer prediction
- `POST /predict/blood` - Dedicated blood cancer detection
- `POST /analyze/blood` - Detailed blood cell analysis

### Model Information
- **Bone Cancer**: Radiomics features + Ensemble ML
- **Lung Cancer**: Vision Transformer with attention maps
- **Blood Cancer**: Graph Neural Network with cell analysis

## 📈 Analytics & Monitoring

### Dashboard Features
- **Real-time Statistics**: Total analyses, confidence scores
- **Model Performance**: Accuracy by model type
- **Usage Trends**: Monthly analysis patterns
- **Diagnosis Distribution**: Cancer vs Normal cases

### History Tracking
- **Complete Analysis History**: All past predictions
- **Filter & Sort**: By organ, date, confidence
- **Export Options**: JSON export for research
- **Detailed Results**: Full explainability data

## 🔍 Explainability Features

### Bone Cancer (Radiomics)
- **SHAP Values**: Feature importance scores
- **Top Features**: Most influential radiomics features
- **Feature Values**: Actual feature measurements

### Lung Cancer (Vision Transformer)
- **Attention Maps**: Visual focus areas
- **Multi-head Attention**: Different attention patterns
- **Token Importance**: Critical image regions

### Blood Cancer (Graph Neural Network)
- **Cell Importance**: Most critical cells
- **Graph Statistics**: Node degrees, clustering
- **Cell Relationships**: Interaction patterns

## 🚀 Advanced Features

### Model Architectures
1. **Radiomics Ensemble**: XGBoost + LightGBM + Random Forest + Neural Network + SVM
2. **Vision Transformer**: Multi-head self-attention with patch-based processing
3. **Graph Neural Network**: Cell detection + relationship modeling + graph convolution

### Training Data
- **Bone Cancer**: Real X-ray images with radiomics annotations
- **Lung Cancer**: Real X-ray images with expert labels
- **Blood Cancer**: Real blood smear images with cell classifications

### Performance Optimization
- **Lazy Loading**: Models loaded on-demand
- **Batch Processing**: Efficient image processing
- **Caching**: Feature extraction optimization
- **Fallback Systems**: Robust error handling

## 📱 Frontend Features

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload
- **Real-time Feedback**: Loading states and progress indicators
- **Modern UI**: Clean, professional medical interface

### Data Visualization
- **Progress Bars**: Confidence visualization
- **Charts**: Analytics and trend visualization
- **Heatmaps**: Attention maps and feature importance
- **Statistics**: Comprehensive performance metrics

## ⚠️ Medical Disclaimer

**IMPORTANT**: This system is for educational and research purposes only. It does not replace professional medical diagnosis. Always consult qualified healthcare professionals for medical decisions.

## 🤝 Contributing

### Development Guidelines
1. **Code Quality**: Follow TypeScript and Python best practices
2. **Testing**: Include unit tests for new features
3. **Documentation**: Update README and API docs
4. **Medical Ethics**: Ensure responsible AI deployment

### Model Training
1. **Data Quality**: Use verified medical datasets
2. **Validation**: Cross-validation and performance testing
3. **Explainability**: Maintain interpretability features
4. **Ethics**: Consider bias and fairness implications

## 📄 License

This project is for educational and research purposes. Please ensure compliance with medical AI regulations and ethical guidelines in your jurisdiction.

## 🙏 Acknowledgments

- **Medical Community**: For providing datasets and expertise
- **AI Research Community**: For advancing medical AI technologies
- **Open Source Contributors**: For tools and libraries used

## 📞 Support

For questions, issues, or contributions:
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check API docs and code comments
- **Community**: Join discussions in issues section

---

**🏥 CancerCare AI - Advanced Cancer Detection System**

*State-of-the-art AI for medical image analysis with explainable results*
