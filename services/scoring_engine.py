from typing import List
from services.jd_parser import extract_skills_from_jd
from services.nlp_engine import compute_nlp_similarity

def compute_final_score(job_description: str, resume_text: str) -> dict:
    """
    Computes a final composite score by combining:
    1. NLP Cosine Similarity
    2. Hard skill matching
    Returns a dictionary with the score details.
    """
    # 1. NLP Similarity (0-100)
    nlp_score = compute_nlp_similarity(job_description, resume_text)
    
    # 2. Skill Extraction
    jd_skills = extract_skills_from_jd(job_description)
    resume_skills = extract_skills_from_jd(resume_text)  # Reusing JD parser to find skills in resume
    
    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    
    # Skill score: percentage of JD skills found in resume
    skill_score = 0.0
    if len(jd_skills) > 0:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
    
    # Composite Score (Weighted: 60% NLP, 40% Exact Skills)
    final_score = int((nlp_score * 0.6) + (skill_score * 0.4))
    
    # Ensure between 0 and 100
    final_score = max(0, min(100, final_score))
    
    return {
        "final_score": final_score,
        "nlp_similarity": nlp_score,
        "skill_match_percentage": skill_score,
        "extracted_jd_skills": jd_skills,
        "matched_skills": matched_skills
    }
