import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

class CandidateEvaluation(BaseModel):
    skills: List[str]
    experience_summary: str
    education_summary: str
    score: int  # 0 to 100
    reasoning: str

def init_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing. Please set it before running.")
    genai.configure(api_key=api_key)

def evaluate_resume(job_description: str, resume_text: str) -> CandidateEvaluation:
    # Use gemini-1.5-flash as it is fast and supports JSON response
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
    
    prompt = f"""
    You are an expert HR Technical Recruiter.
    Your task is to evaluate the provided Resume against the provided Job Description.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume_text}
    
    Please extract the candidate's skills, a short summary of their experience, and a short summary of their education.
    Then, compute a relevance score from 0 to 100 based on how well the candidate's resume matches the Job Description.
    Finally, provide a clear reasoning for the score.
    
    Return the result strictly as a JSON object with the following keys:
    - "skills": A list of strings representing extracted skills.
    - "experience_summary": A string summarizing their experience.
    - "education_summary": A string summarizing their education.
    - "score": An integer between 0 and 100.
    - "reasoning": A concise string explaining why this score was given.
    """
    
    response = model.generate_content(prompt)
    try:
        data = json.loads(response.text)
        # Validate and return using Pydantic
        return CandidateEvaluation(**data)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}\nResponse was: {response.text}")
        raise ValueError("Failed to parse Gemini API response as expected JSON.")
