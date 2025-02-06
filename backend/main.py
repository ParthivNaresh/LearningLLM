from fastapi import FastAPI
from threading import Lock
from backend.api import API

# Create FastAPI app
app = FastAPI()

# Lock to ensure thread safety
queue_lock = Lock()

# Initialize API and register routes
api = API(app, queue_lock)

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
