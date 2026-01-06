from fastapi import FastAPI
from app.routes.predict import router as predict_router
app = FastAPI(
    title="Bone Cancer Detection API",
    description="Backend API for bone cancer detection using ML",
    version="1.0"
)

app.include_router(predict_router)

@app.get("/")
def root():
    return {"status": "Backend is running successfully"}
