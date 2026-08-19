import re
from typing import List

def extract_skills_from_jd(jd_text: str) -> List[str]:
    """
    Very basic heuristic-based JD parser that looks for common tech skills.
    In a real-world scenario, this could use a sophisticated NER model like SpaCy,
    but for this 24hr challenge, we use a predefined dictionary mapping or simple regex.
    """
    common_skills = [
        "python", "java", "c++", "fastapi", "flask", "django", "react", "next.js", 
        "node.js", "javascript", "typescript", "sql", "postgresql", "mysql", "mongodb",
        "nosql", "aws", "gcp", "azure", "docker", "kubernetes", "ci/cd", "git", "bash"
    ]
    
    extracted = set()
    lower_jd = jd_text.lower()
    
    for skill in common_skills:
        # Simple word boundary regex to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, lower_jd):
            extracted.add(skill)
            
    return list(extracted)
