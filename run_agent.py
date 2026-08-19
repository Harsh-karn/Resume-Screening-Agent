import os
import json
from services.file_parser import extract_text_from_file
from services.scoring_engine import compute_final_score
from services.gemini_service import generate_reasoning, init_gemini

def main():
    print("Starting Resume Screening Agent CLI...")
    
    # Initialize Gemini API configuration
    try:
        init_gemini()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return
    
    jd_path = os.path.join("data", "jd.txt")
    resumes_dir = os.path.join("data", "resumes")
    
    # Check if data exists
    if not os.path.exists(jd_path) or not os.path.exists(resumes_dir):
        print("Error: Missing data/jd.txt or data/resumes/ directory.")
        return

    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()
        
    print(f"Loaded Job Description from {jd_path}")
    print("Evaluating Resumes (Multi-Stage Pipeline)...\n")
    
    results = []
    
    for filename in os.listdir(resumes_dir):
        file_path = os.path.join(resumes_dir, filename)
        if os.path.isfile(file_path):
            print(f"Processing {filename}...")
            
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                
            try:
                resume_text = extract_text_from_file(filename, file_bytes)
                
                # 1. NLP Similarity & Scoring Engine
                score_data = compute_final_score(job_description, resume_text)
                
                # 2. Gemini Reasoning Engine
                evaluation = generate_reasoning(job_description, resume_text, score_data)
                
                # Append to results
                results.append({
                    "filename": filename,
                    "evaluation": evaluation.model_dump()
                })
            except Exception as e:
                print(f"Failed to evaluate {filename}: {e}")
                
    # Rank candidates by score descending
    results.sort(key=lambda x: x["evaluation"].get("score", 0), reverse=True)
    
    output_json = {
        "job_description_snippet": job_description[:100] + "...",
        "candidates": results
    }
    
    output_file = "final_ranked_candidates.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=4)
        
    print(f"\nDone! Ranked list saved to {output_file}")
    
    print("\n--- Top Candidate ---")
    if results:
        top = results[0]
        print(f"Name/File: {top['filename']}")
        print(f"Score: {top['evaluation']['score']}")
        print(f"Reasoning: {top['evaluation']['reasoning']}")

if __name__ == "__main__":
    main()
