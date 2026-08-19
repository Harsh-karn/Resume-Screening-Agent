# Resume Screening Agent - ROOMAN AI CHALLENGE

This repository contains an end-to-end Resume Screening Agent built for the ROOMAN AI CHALLENGE. 

## Expected Capabilities
- Parses resumes (`.txt`, `.pdf`, `.docx`) to extract skills, experience, and education.
- Computes a relevance score (0-100) against a provided Job Description using Google Gemini 1.5 Flash.
- Outputs a scored, ordered list of candidates with transparent reasoning for the score.

## Tech Stack
- **Python 3**
- **FastAPI** & **Uvicorn** (for the backend API)
- **Google Generative AI SDK** (for the Gemini model integration)
- **pypdf** & **python-docx** (for document parsing)

## Setup Instructions

1. **Clone the repository** (or navigate to the folder):
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd ROOMAN AI CHALLENGE
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**:
   Get a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).
   Create a `.env` file in the root directory and add your key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```

## Running the Agent (CLI - Recommended)

The easiest way to test the agent is via the command-line script. It will read the dummy JD and resumes from the `data/` folder, evaluate them using Gemini, rank them, and output a `final_ranked_candidates.json` file.

```bash
python run_agent.py
```

## Running the Agent (FastAPI Backend)

Alternatively, you can start the FastAPI backend server to serve this as a REST API.

```bash
python main.py
# Or run using uvicorn directly: uvicorn main:app --reload
```

The server will start on `http://0.0.0.0:8000`.

## Testing via API & Sample Inputs/Outputs

A set of dummy data is provided in the `data/` folder:
- `data/jd.txt`: A sample Job Description for a Python Backend Developer.
- `data/resumes/`: Contains 3 dummy resumes with varying levels of fit for the role.

**How to Test via Swagger UI:**
1. Open your browser and go to `http://localhost:8000/docs`.
2. Expand the `POST /api/v1/screen-resumes` endpoint and click **Try it out**.
3. In the `job_description` field, paste the text from `data/jd.txt`.
4. In the `resumes` field, click **Add string item** (this UI button allows adding multiple files in Swagger) and upload the files from `data/resumes/`.
5. Click **Execute**.
6. Scroll down to see the JSON output, which will rank the candidates from highest to lowest score with extracted details and reasoning.

## Tradeoffs and Design Decisions

- **Model Choice:** I used `gemini-1.5-flash` instead of a local model or OpenAI to balance speed, cost (it's free for developers), and quality. It is excellent at following structured JSON schemas.
- **Scoring Logic (NLP vs LLM):** Instead of using basic NLP embeddings (like cosine similarity), I used the LLM itself as an evaluator. This is typically more robust because the LLM can understand the *context* of experience (e.g., managing a database vs. just listing "PostgreSQL" as a keyword).
- **Interface:** I chose a FastAPI backend. This allows for a clean separation of concerns and makes the agent ready to be integrated into any frontend (React, Streamlit, etc.) easily via a standard REST API.
- **Future Improvements:** With more time, I would implement a Retrieval-Augmented Generation (RAG) approach to pre-filter resumes if the list was massive (e.g., 10,000+ resumes). I would also add more comprehensive error handling and logging for corrupted PDF files.
