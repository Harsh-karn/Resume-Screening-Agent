from typing import Dict
from services.nlp_engine import compute_nlp_similarity

def compute_final_score(job_description: str, resume_text: str, jd_features: Dict, resume_features: Dict) -> dict:
    """
    Computes a final composite score by combining:
    1. NLP Cosine Similarity on raw text
    2. Hard skill matching
    3. Experience match heuristic
    """
    # 1. NLP Similarity (0-100)
    nlp_score = compute_nlp_similarity(job_description, resume_text)
    
    # 2. Skill Extraction Matching
    jd_skills = jd_features.get("skills", [])
    resume_skills = resume_features.get("skills", [])
    
    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    
    skill_score = 0.0
    if len(jd_skills) > 0:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
        
    # 3. Experience Match Heuristic
    # Very basic: if JD asks for 'years' and resume experience section is not empty, give a small boost.
    # In a real model, this would parse out the exact years.
    exp_boost = 0
    if "years" in jd_features.get("experience", ""):
        if len(resume_features.get("experience", "")) > 50:
            exp_boost = 10  # Boost for having substantial experience section
    
    # Composite Score (Weighted: 50% NLP, 40% Exact Skills, 10% Experience Boost)
    final_score = int((nlp_score * 0.5) + (skill_score * 0.4) + exp_boost)
    
    # Ensure between 0 and 100
    final_score = max(0, min(100, final_score))
    
    return {
        "final_score": final_score,
        "nlp_similarity": nlp_score,
        "skill_match_percentage": skill_score,
        "extracted_jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "resume_experience": resume_features.get("experience", ""),
        "resume_education": resume_features.get("education", "")
    }
