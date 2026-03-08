from app.services.organ_classifier import predict_organ

# Put a real image path here
IMAGE_PATH = "test_image.jpg"

with open(IMAGE_PATH, "rb") as f:
    result = predict_organ(f.read())

print("ORGAN PREDICTION RESULT:")
print(result)
