import re
from typing import Dict, List

def extract_features_from_jd(jd_text: str) -> Dict[str, any]:
    """
    Extracts structured requirements (skills, experience) from the JD.
    """
    common_skills = [
        "python", "java", "c++", "fastapi", "flask", "django", "react", "next.js", 
        "node.js", "javascript", "typescript", "sql", "postgresql", "mysql", "mongodb",
        "nosql", "aws", "gcp", "azure", "docker", "kubernetes", "ci/cd", "git", "bash"
    ]
    
    extracted_skills = set()
    lower_jd = jd_text.lower()
    
    for skill in common_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, lower_jd):
            extracted_skills.add(skill)
            
    # Basic heuristic for required years of experience
    exp_match = re.search(r'(\d+)\+?\s*years', lower_jd)
    experience_req = f"{exp_match.group(1)}+ years" if exp_match else "Not explicitly stated"
            
    return {
        "skills": list(extracted_skills),
        "experience": experience_req
    }
