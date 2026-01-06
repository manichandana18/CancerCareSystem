# Bone Cancer Detection System

A machine learning-based system for detecting bone cancer from X-ray images, built with Java frontend and Python FastAPI backend.

## Project Structure

```
BONE CANCER/
├── src/                    # Java frontend application
│   ├── Main.java          # Main entry point
│   ├── api/               # API client for Python backend
│   ├── detection/         # Cancer detection logic
│   ├── preprocessing/     # Image preprocessing
│   ├── text/              # Textual information generator
│   └── utils/             # Utility functions
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── main.py        # FastAPI application
│   │   ├── models/        # Model training scripts
│   │   ├── routes/        # API routes
│   │   └── services/      # Prediction services
│   └── dataset/           # Training dataset
│       ├── normal/        # Normal X-ray images
│       └── tumor/         # Tumor X-ray images
└── sample_xray.jpg        # Sample X-ray image for testing
```

## Prerequisites

### Java
- Java JDK 8 or higher
- Java compiler (javac)

### Python
- Python 3.8 or higher
- pip package manager

## Setup Instructions

### Backend Setup (Python)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Train the model (optional - if you have dataset):
   ```bash
   python app/models/train_model.py
   ```
   This will create `bone_cancer_model.h5` in the backend directory.

6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   The API will be available at: `http://127.0.0.1:8000`

### Frontend Setup (Java)

1. Compile the Java files:
   ```bash
   cd src
   javac -d .. Main.java
   ```

2. Run the application:
   ```bash
   cd ..
   java Main [image_path]
   ```
   
   Example:
   ```bash
   java Main sample_xray.jpg
   ```

## Usage

1. **Start the Python backend** (see Backend Setup above)

2. **Run the Java frontend**:
   ```bash
   java Main sample_xray.jpg
   ```

3. The system will:
   - Load and validate the image
   - Send it to the Python backend API
   - Receive prediction results
   - Display textual information and advice

## API Endpoints

### POST `/predict`
Upload an X-ray image for bone cancer detection.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file)

**Response:**
```json
{
  "prediction": "Tumor Detected" | "No Tumor Detected",
  "confidence": 0.85,
  "advice": [
    "Consult a specialist",
    "Early detection helps",
    "Stay strong and positive"
  ]
}
```

### GET `/`
Health check endpoint.

**Response:**
```json
{
  "status": "Backend is running successfully"
}
```

## Model Training

To train your own model:

1. Place your dataset in `backend/dataset/`:
   - `normal/` - Normal X-ray images
   - `tumor/` - Tumor X-ray images

2. Run the training script:
   ```bash
   python backend/app/models/train_model.py
   ```

3. The trained model will be saved as `bone_cancer_model.h5`

## Features

- ✅ Image loading and validation
- ✅ RESTful API for predictions
- ✅ Machine learning model integration
- ✅ User-friendly textual output
- ✅ Error handling and validation
- ✅ Support for multiple image formats (JPG, JPEG, PNG, BMP)

## Troubleshooting

### Backend Issues
- **Port already in use**: Change the port in the uvicorn command
- **Model not found**: The system will use a fallback prediction method
- **Import errors**: Make sure all dependencies are installed via `pip install -r requirements.txt`

### Frontend Issues
- **Image not found**: Ensure the image path is correct and the file exists
- **Connection error**: Make sure the Python backend is running on port 8000
- **Compilation errors**: Ensure all Java files are in the correct package structure

## Next Steps

After completing the program modifications:

1. **Test the system**:
   - Start the backend server
   - Run the Java frontend with a test image
   - Verify predictions are working

2. **Train your model**:
   - Add your dataset to `backend/dataset/`
   - Train the model using `train_model.py`
   - The system will automatically use the trained model

3. **Deploy** (optional):
   - Deploy the Python backend to a cloud service
   - Update the API URL in `PythonAPIClient.java`
   - Package the Java application for distribution

4. **Enhancements** (optional):
   - Add database for storing predictions
   - Implement user authentication
   - Add web interface
   - Improve model accuracy with more data

## License

This project is for educational and research purposes.

## Disclaimer

This system is for educational purposes only and should not be used as a substitute for professional medical diagnosis. Always consult qualified healthcare professionals for medical advice.


