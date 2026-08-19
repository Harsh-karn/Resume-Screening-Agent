from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
import uvicorn

from services.file_parser import extract_text_from_file
from services.scoring_engine import compute_final_score
from services.gemini_service import generate_reasoning, init_gemini
from services.models import CandidateEvaluation

app = FastAPI(
    title="Resume Screening Agent",
    description="An AI agent to rank resumes against a Job Description",
    version="1.0.0"
)

# Initialize Gemini API on startup
@app.on_event("startup")
async def startup_event():
    try:
        init_gemini()
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini API: {e}")

@app.post("/api/v1/screen-resumes")
async def screen_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
        
    results = []
    
    for resume in resumes:
        try:
            file_bytes = await resume.read()
            resume_text = extract_text_from_file(resume.filename, file_bytes)
            
            # 1. NLP Similarity & Scoring Engine
            score_data = compute_final_score(job_description, resume_text)
            
            # 2. Gemini Reasoning Engine
            evaluation = generate_reasoning(job_description, resume_text, score_data)
            
            results.append({
                "filename": resume.filename,
                "evaluation": evaluation.model_dump()
            })
        except Exception as e:
            results.append({
                "filename": resume.filename,
                "error": str(e)
            })
            
    # Sort by score descending
    results.sort(key=lambda x: x.get("evaluation", {}).get("score", 0), reverse=True)
    
    output_json = {
        "job_description_snippet": job_description[:100] + "...",
        "candidates": results
    }
    
    return output_json

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
