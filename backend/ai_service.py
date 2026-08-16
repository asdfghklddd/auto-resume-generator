import os
import json
from google import genai
from .schemas import ResumeData

def generate_resume_from_text(raw_text: str) -> ResumeData:
    """
    Calls Google Gemini using the structured output feature to transform 
    messy raw text into a highly polished, STAR-format ResumeData JSON.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY environment variable is not set correctly.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an elite executive resume writer and career coach. Your task is to take the following raw, messy user input and completely transform it into a highly professional, polished resume.
    
    CRITICAL INSTRUCTIONS:
    1. Parse the input and identify all jobs, education, projects, and skills.
    2. If a section is brief (e.g., "worked at McDonald's"), expand it slightly into professional terminology but DO NOT wildly hallucinate responsibilities they never had. Keep it realistic but impressive.
    3. For all experience and project highlights, you MUST rewrite them using the STAR method (Situation, Task, Action, Result). Start bullet points with strong action verbs (e.g., Orchestrated, Architected, Spearheaded, Developed).
    4. Provide a compelling 2-3 sentence professional summary based on their overall profile.
    5. Ensure the output strictly adheres to the requested JSON schema.
    
    RAW USER INPUT:
    ---
    {raw_text}
    ---
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ResumeData,
            "temperature": 0.4,
        },
    )
    # Pydantic validates the provider response before it reaches the client.
    json_data = json.loads(response.text)
    return ResumeData(**json_data)
