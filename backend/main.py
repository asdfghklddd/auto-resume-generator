import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .ai_service import generate_resume_from_text
from .schemas import ResumeData

load_dotenv()

app = FastAPI(title="Auto Resume Generator API")

# Single-Prompt Architecture safeguard limit (1 request at a time against Gemini Free Tier)
gemini_semaphore = asyncio.Semaphore(1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RawInputRequest(BaseModel):
    text: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running!"}

@app.post("/api/generate", response_model=ResumeData)
async def generate_resume_endpoint(request: RawInputRequest):
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Please provide more details in the input box.")
        
    try:
        # Prevent overwhelming the free-tier API
        async with gemini_semaphore:
            # Run the synchronous SDK call in a threadpool to not block the asyncio event loop
            resume_data = await asyncio.to_thread(generate_resume_from_text, request.text)
            return resume_data
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Processing failed: {str(e)}")

# Serve the frontend static files if they exist
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{catchall:path}")
    async def serve_frontend(catchall: str):
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
