import re
from typing import Dict, List
from services.jd_parser import extract_features_from_jd

def extract_section(text: str, headers: List[str]) -> str:
    """
    Very basic heuristic to extract a section based on common headers.
    Finds a header and extracts everything until the next likely header.
    """
    lower_text = text.lower()
    start_idx = -1
    for header in headers:
        idx = lower_text.find(header.lower())
        if idx != -1:
            start_idx = idx + len(header)
            break
            
    if start_idx == -1:
        return ""
        
    # Find next double newline or likely next section
    remaining = text[start_idx:]
    next_header_match = re.search(r'\n\s*[A-Z][A-Za-z]+\s*:\s*\n', remaining)
    
    if next_header_match:
        end_idx = next_header_match.start()
        return remaining[:end_idx].strip()
    else:
        # If no obvious next header, just take the next 1000 chars as a heuristic
        return remaining[:1000].strip()

def extract_resume_features(resume_text: str) -> Dict[str, any]:
    """
    Extracts distinct features from the raw resume text:
    - skills: list of strings
    - experience: string block
    - education: string block
    """
    # Use existing heuristic logic for technical skills
    features = extract_features_from_jd(resume_text)
    skills = features["skills"]
    
    experience = extract_section(resume_text, ["experience", "employment", "work history"])
    education = extract_section(resume_text, ["education", "academic background", "university"])
    
    return {
        "skills": skills,
        "experience": experience,
        "education": education
    }
