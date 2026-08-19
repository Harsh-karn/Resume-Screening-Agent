from pydantic import BaseModel
from typing import List

class CandidateEvaluation(BaseModel):
    skills: List[str]
    experience_summary: str
    education_summary: str
    score: int  # 0 to 100
    reasoning: str
