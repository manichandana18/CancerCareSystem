from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Minimal path setup
sys.path.append(os.getcwd())

from app.routes.auth import router as auth_router

app = FastAPI(title="Emergency Auth Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"status": "Emergency Auth Server Running"}

if __name__ == "__main__":
    print("🚀 Starting EMERGENCY AUTH SERVER on port 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
