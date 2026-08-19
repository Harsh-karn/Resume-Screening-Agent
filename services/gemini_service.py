import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

class CandidateEvaluation(BaseModel):
    skills: List[str]
    experience_summary: str
    education_summary: str
    score: int  # 0 to 100
    reasoning: str

def init_gemini():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing. Please set it before running.")
    genai.configure(api_key=api_key)

def generate_reasoning(job_description: str, resume_text: str, score_data: dict) -> CandidateEvaluation:
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    
    final_score = score_data.get("final_score", 0)
    matched_skills = score_data.get("matched_skills", [])
    nlp_similarity = score_data.get("nlp_similarity", 0.0)
    resume_experience = score_data.get("resume_experience", "Not found.")
    resume_education = score_data.get("resume_education", "Not found.")
    
    prompt = f"""
    You are an expert HR Technical Recruiter.
    We have already calculated a relevance score for this candidate using an NLP Engine and a Scoring Engine.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    Pre-Calculated Metrics:
    - Final Score: {final_score}/100
    - NLP Cosine Similarity: {nlp_similarity}%
    - Hard Skills Matched: {matched_skills}
    - Extracted Experience Block: {resume_experience}
    - Extracted Education Block: {resume_education}
    
    Your task is to:
    1. Extract a short summary of the candidate's experience.
    2. Extract a short summary of the candidate's education.
    3. Provide a clear, concise reasoning for why this candidate received a score of {final_score}/100 based on the metrics above and the resume contents.
    
    Return the result strictly as a JSON object with the following keys:
    - "skills": The list of Hard Skills Matched provided above.
    - "experience_summary": A string summarizing their experience.
    - "education_summary": A string summarizing their education.
    - "score": The Final Score provided above as an integer.
    - "reasoning": A concise string explaining why this score makes sense.
    """
    
    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text)
        return CandidateEvaluation(**data)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        # Fallback if Gemini fails entirely (which happens for AQ. internal keys)
        return CandidateEvaluation(
            skills=matched_skills,
            experience_summary=resume_experience[:200] + "..." if len(resume_experience) > 200 else resume_experience,
            education_summary=resume_education[:200] + "..." if len(resume_education) > 200 else resume_education,
            score=final_score,
            reasoning=f"Candidate achieved an NLP similarity of {nlp_similarity}% and matched skills: {matched_skills}."
        )
