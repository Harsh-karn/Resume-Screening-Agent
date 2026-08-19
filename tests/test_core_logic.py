import pytest
from services.jd_parser import extract_features_from_jd
from services.feature_extractor import extract_resume_features
from services.scoring_engine import compute_final_score

def test_extract_features_from_jd():
    # Arrange
    jd_text = "We are looking for a Software Engineer with 3+ years of experience in Python, Django, and PostgreSQL."
    
    # Act
    features = extract_features_from_jd(jd_text)
    
    # Assert
    assert "python" in features["skills"]
    assert "django" in features["skills"]
    assert "postgresql" in features["skills"]
    assert "years" in features["experience"]

def test_extract_resume_features():
    # Arrange
    resume_text = """
    John Doe
    Skills: Python, React, Docker, Kubernetes
    Experience: 
    Worked at TechCorp for 5 years building scalable APIs.
    Education:
    B.S. Computer Science from University of Tech
    """
    
    # Act
    features = extract_resume_features(resume_text)
    
    # Assert
    assert "python" in features["skills"]
    assert "react" in features["skills"]
    assert "docker" in features["skills"]
    assert "techcorp for 5 years" in features["experience"].lower()
    assert "computer science" in features["education"].lower()

def test_compute_final_score():
    # Arrange
    jd_text = "Looking for Python, React, and Docker experience."
    resume_text = "I know Python, React, and Docker. I have built many things."
    
    jd_features = extract_features_from_jd(jd_text)
    resume_features = extract_resume_features(resume_text)
    
    # Act
    score_data = compute_final_score(jd_text, resume_text, jd_features, resume_features)
    
    # Assert
    assert score_data["final_score"] > 0
    assert score_data["final_score"] <= 100
    assert "python" in score_data["matched_skills"]
    assert "react" in score_data["matched_skills"]
    assert "docker" in score_data["matched_skills"]
    assert score_data["nlp_similarity"] > 0

def test_scoring_handles_missing_skills():
    # Arrange
    jd_text = "Looking for Java and Spring Boot."
    resume_text = "I only know Python and Django."
    
    jd_features = extract_features_from_jd(jd_text)
    resume_features = extract_resume_features(resume_text)
    
    # Act
    score_data = compute_final_score(jd_text, resume_text, jd_features, resume_features)
    
    # Assert
    # Low score since no hard skills matched and similarity is low
    assert len(score_data["matched_skills"]) == 0
    assert score_data["final_score"] < 50
