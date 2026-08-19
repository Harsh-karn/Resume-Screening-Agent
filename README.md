# Resume Screening AI Agent

An autonomous, multi-stage NLP agent built for the Rooman AI Challenge that ranks a set of resumes against a given Job Description and outputs an ordered shortlist with conversational AI reasoning.

## Architecture

This project implements a multi-stage architecture to ensure deterministic, reproducible scoring combined with LLM-powered conversational reasoning:

```text
             Job Description
                    │
                    ▼
          ┌──────────────────┐
          │ JD Parser        │
          │ (Extracts Skills)│
          └────────┬─────────┘
                   │
                   ▼
Resumes ──► Resume Parser (PDF/DOCX/TXT text extraction)
                   │
                   ▼
          ┌──────────────────┐
          │ Feature Extractor│
          │ (skills, exp,    │
          │  education)      │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ NLP Engine       │
          │ (TF-IDF Cosine   │
          │  Similarity)     │
          └────────┬─────────┘
                   │
                   ▼
          Scoring Engine (Weighted aggregation of NLP + Hard Skills)
                   │
                   ▼
        Ranked Candidates
                   │
                   ▼
       Gemini LLM (Generates conversational "Reasoning" for the score)
```

## Setup Instructions (Foolproof)

This project has explicitly pinned dependencies to guarantee it runs flawlessly out of the box.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Harsh-karn/Resume-Screening-Agent.git
   cd Resume-Screening-Agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Pinned Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables:**
   Create a `.env` file in the root of the project and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_standard_gemini_api_key_here
   ```

## How to Run

### Option 1: Automated CLI (End-to-End Workflow)
The easiest way to evaluate the sample data provided in the `data/` folder.
```bash
python run_agent.py
```
This will read the `data/jd.txt`, iterate over all resumes in `data/resumes/`, process them through the multi-stage NLP pipeline, and output the final rankings to `final_ranked_candidates.json`.

### Option 2: FastAPI Web Server
You can also run the agent as a web service.
```bash
uvicorn main:app --reload
```
Navigate to `http://127.0.0.1:8000/docs` to use the Swagger UI to upload your own Job Description and PDF/DOCX resumes dynamically.

## Design Decisions & Tradeoffs

1. **Deterministic NLP vs. Pure LLM:** 
   *Tradeoff:* Initially, we considered passing the entire JD and Resume directly to Gemini to generate a score. However, LLMs can hallucinate scores and are notoriously non-deterministic.
   *Decision:* We explicitly built an NLP Engine (`scikit-learn` TF-IDF Cosine Similarity) and a Scoring Engine. This guarantees that candidates are scored mathematically and fairly based on keyword overlap and semantic similarity. Gemini is strictly used at the very end of the pipeline to generate conversational, human-readable *reasoning* for that deterministic score.
2. **Lightweight NLP Engine:**
   *Tradeoff:* We could have used heavy PyTorch models (like `sentence-transformers`) for incredibly dense vector embeddings.
   *Decision:* To make setup foolproof and fast for reviewers, we opted for `scikit-learn`'s `TfidfVectorizer`. It provides excellent text similarity scoring without requiring a 5GB PyTorch installation or GPU hardware.
3. **Robust LLM Fallbacks:**
   *Tradeoff:* Relying entirely on an external API can cause the application to crash if rate limits are hit or network drops occur.
   *Decision:* We implemented a `try/except` fallback in `gemini_service.py`. If the Gemini API fails, the application automatically constructs a structured fallback response using the explicitly extracted features from our `feature_extractor.py` step, ensuring the pipeline completes gracefully.

## Limitations & Future Work

- **Heuristic Feature Extraction:** Currently, the `feature_extractor.py` uses basic heuristics and keyword lookups to parse `experience` and `education` blocks. While effective for standard resumes, it can struggle with highly unconventional resume formats. *Future Work:* Replace this heuristics layer with a dedicated small-scale NER (Named Entity Recognition) model using `spaCy`.
- **SDK Deprecation:** We are currently using the `google-generativeai` package, which is actively displaying a deprecation warning in favor of `google.genai`. *Future Work:* Migrate the API calls to the new SDK standard once it stabilizes.
- **Complex PDF Formatting:** `pypdf` struggles with two-column resume layouts, sometimes reading text left-to-right across columns instead of top-to-bottom. *Future Work:* Implement a layout-aware PDF parser (like `pdfplumber`) to handle complex visual resumes better.
