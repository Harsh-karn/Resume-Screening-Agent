from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text: str) -> str:
    """Basic NLP text cleaning: lowercase and remove non-alphanumeric chars."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def compute_nlp_similarity(job_description: str, resume_text: str) -> float:
    """
    Computes a Cosine Similarity score between the Job Description and Resume
    using a TF-IDF Vectorizer. Returns a float between 0.0 and 100.0.
    """
    jd_clean = clean_text(job_description)
    resume_clean = clean_text(resume_text)
    
    # Create the vectorizer and fit on both documents to build vocabulary
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform([jd_clean, resume_clean])
        # Compute cosine similarity between the two vectors (index 0 and index 1)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)
    except Exception as e:
        print(f"Error computing NLP similarity: {e}")
        return 0.0
