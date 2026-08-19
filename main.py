from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn

from services.file_parser import extract_text_from_file
from services.gemini_service import init_gemini, evaluate_resume, CandidateEvaluation

app = FastAPI(
    title="Resume Screening Agent",
    description="An AI agent that evaluates resumes against a Job Description using Google Gemini.",
    version="1.0.0"
)

# Initialize Gemini on startup
@app.on_event("startup")
def startup_event():
    try:
        init_gemini()
        print("Gemini API initialized successfully.")
    except Exception as e:
        print(f"Warning on startup: {e}")

class RankedCandidate(BaseModel):
    filename: str
    evaluation: CandidateEvaluation

class RankingResponse(BaseModel):
    job_description: str
    candidates: List[RankedCandidate]

@app.post("/api/v1/screen-resumes", response_model=RankingResponse)
async def screen_resumes(
    job_description: str = Form(..., description="The Job Description text to evaluate against."),
    resumes: List[UploadFile] = File(..., description="List of resume files (PDF, DOCX, TXT).")
):
    """
    Endpoint to evaluate and rank a list of resumes against a given Job Description.
    """
    if not resumes:
        raise HTTPException(status_code=400, detail="No resumes provided.")

    ranked_candidates = []
    
    for resume in resumes:
        try:
            file_bytes = await resume.read()
            resume_text = extract_text_from_file(resume.filename, file_bytes)
            
            # Evaluate using Gemini
            evaluation = evaluate_resume(job_description, resume_text)
            
            ranked_candidates.append(
                RankedCandidate(
                    filename=resume.filename,
                    evaluation=evaluation
                )
            )
        except Exception as e:
            # You might want to log this and continue with other files, 
            # but for simplicity, we'll raise an HTTP exception or just append the error
            print(f"Error processing {resume.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process {resume.filename}: {str(e)}")
            
    # Sort candidates by score descending
    ranked_candidates.sort(key=lambda x: x.evaluation.score, reverse=True)
    
    return RankingResponse(
        job_description=job_description,
        candidates=ranked_candidates
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
