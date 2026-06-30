# AI Career Copilot

A resume/career assistant with 9 features (resume feedback, skill gap analysis,
bullet rewriting, full resume improvement, cover letters, interview questions,
career suggestions, ATS score explanation, and profile summaries), powered by
the Cohere API.

## Architecture

- `prompts.py` — all prompt templates, shared by the backend.
- `backend.py` — FastAPI server with one endpoint per feature. Calls Cohere's
  chat API.
- `colab_backend.ipynb` — runs `backend.py` inside Google Colab and exposes
  it publicly via `pyngrok`, so you don't need your own server.
- `streamlit_app.py` — the web frontend. Calls the backend over HTTP.

## How to run it

### 1. Start the backend in Google Colab

1. Open [Google Colab](https://colab.research.google.com) and upload
   `colab_backend.ipynb`.
2. In the Colab file browser (left sidebar), also upload `backend.py` and
   `prompts.py` into the same Colab session.
3. Run all cells top to bottom. You'll be asked for:
   - Your **Cohere API key** (get one free at https://dashboard.cohere.com/api-keys)
   - Your **ngrok authtoken** (get one free at https://dashboard.ngrok.com/get-started/your-authtoken)
4. The last cell starts the server and prints a public URL like
   `https://abcd-1234.ngrok-free.app`. Keep this notebook running — closing
   it or letting Colab disconnect will take the backend down.

### 2. Run the Streamlit frontend (on your own machine)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

In the sidebar, paste the ngrok URL from step 1. The sidebar will show
"Connected to backend ✅" once it can reach it. Then pick a feature, paste
your resume/job description, and run it.

### Running the backend locally instead of Colab (optional)

```bash
pip install -r requirements.txt
export COHERE_API_KEY=your_key_here
uvicorn backend:app --reload --port 8000
```

Then point the Streamlit sidebar at `http://localhost:8000`.

## Notes

- The Colab + ngrok backend URL changes every time you restart the notebook
  (unless you have a paid ngrok static domain) — just paste the new URL into
  Streamlit's sidebar each time.
- Cohere's free trial keys are rate-limited; if you hit errors under load,
  check your usage at https://dashboard.cohere.com.
- The bullet-rewriting and resume-improving prompts are instructed not to
  invent metrics that aren't implied by your original text — they'll insert
  `[ADD METRIC]` placeholders instead of fabricating numbers.
