"""
AI Career Copilot — Streamlit Frontend

Run locally:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

Then paste the backend's public URL (from the Colab notebook / ngrok) into
the sidebar field, e.g. https://abcd-1234.ngrok-free.app
"""

import requests
import streamlit as st

st.set_page_config(page_title="AI Career Copilot", page_icon="🧠", layout="wide")

# ---------------------------------------------------------------------------
# Sidebar — backend connection
# ---------------------------------------------------------------------------

st.sidebar.title("⚙️ Settings")
backend_url = st.sidebar.text_input(
    "Backend URL (from Colab/ngrok)",
    placeholder="https://your-ngrok-url.ngrok-free.app",
).rstrip("/")

if backend_url:
    try:
        health = requests.get(backend_url + "/", timeout=5)
        if health.ok:
            st.sidebar.success("Connected to backend ✅")
        else:
            st.sidebar.error(f"Backend responded with status {health.status_code}")
    except Exception:
        st.sidebar.error("Could not reach backend. Check the URL.")
else:
    st.sidebar.warning("Paste your backend URL to get started.")

feature = st.sidebar.radio(
    "Choose a feature",
    [
        "Resume Feedback",
        "Skill Gap Analysis",
        "Rewrite Bullet Points",
        "Full Resume Improver",
        "Cover Letter Generator",
        "Interview Question Generator",
        "Career Suggestions",
        "ATS Score Explanation",
        "Final Summary",
    ],
)

st.title("🧠 AI Career Copilot")
st.caption("Resume, job search, and interview prep tools powered by Cohere.")


def call_backend(endpoint: str, payload: dict) -> str:
    if not backend_url:
        st.error("Set the backend URL in the sidebar first.")
        return ""
    try:
        resp = requests.post(f"{backend_url}{endpoint}", json=payload, timeout=120)
        if resp.status_code != 200:
            st.error(f"Backend error ({resp.status_code}): {resp.json().get('detail', resp.text)}")
            return ""
        return resp.json().get("result", "")
    except requests.exceptions.Timeout:
        st.error("Request timed out. The model may be taking too long — try again.")
        return ""
    except Exception as exc:
        st.error(f"Request failed: {exc}")
        return ""


# ---------------------------------------------------------------------------
# Shared input widgets
# ---------------------------------------------------------------------------

def resume_and_jd_inputs(jd_required: bool = False):
    resume_text = st.text_area("Paste your resume text", height=250)
    jd_label = "Paste the job description" + (" (required)" if jd_required else " (optional)")
    job_description = st.text_area(jd_label, height=200)
    return resume_text, job_description


# ---------------------------------------------------------------------------
# Feature pages
# ---------------------------------------------------------------------------

if feature == "Resume Feedback":
    st.subheader("📋 Resume Feedback")
    resume_text, job_description = resume_and_jd_inputs()
    if st.button("Analyze Resume", type="primary"):
        if not resume_text.strip():
            st.warning("Paste a resume first.")
        else:
            with st.spinner("Analyzing..."):
                result = call_backend("/resume-feedback", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "Skill Gap Analysis":
    st.subheader("🧩 Skill Gap Analysis")
    resume_text, job_description = resume_and_jd_inputs(jd_required=True)
    if st.button("Find Skill Gaps", type="primary"):
        if not resume_text.strip() or not job_description.strip():
            st.warning("Both resume and job description are required.")
        else:
            with st.spinner("Comparing..."):
                result = call_backend("/skill-gap", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "Rewrite Bullet Points":
    st.subheader("✍️ Rewrite Bullet Points")
    bullet_points = st.text_area("Paste bullet points to improve (one per line)", height=200)
    job_description = st.text_area("Job description (optional, helps tailor the rewrite)", height=150)
    if st.button("Rewrite", type="primary"):
        if not bullet_points.strip():
            st.warning("Paste some bullet points first.")
        else:
            with st.spinner("Rewriting..."):
                result = call_backend("/rewrite-bullets", {"bullet_points": bullet_points, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "Full Resume Improver":
    st.subheader("📄 Full Resume Improver")
    resume_text, job_description = resume_and_jd_inputs()
    if st.button("Improve Full Resume", type="primary"):
        if not resume_text.strip():
            st.warning("Paste a resume first.")
        else:
            with st.spinner("Improving..."):
                result = call_backend("/improve-resume", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "Cover Letter Generator":
    st.subheader("💌 Cover Letter Generator")
    resume_text = st.text_area("Paste your resume text", height=250)
    job_description = st.text_area("Paste the job description", height=200)
    company_name = st.text_input("Company name (optional)")
    if st.button("Generate Cover Letter", type="primary"):
        if not resume_text.strip() or not job_description.strip():
            st.warning("Both resume and job description are required.")
        else:
            with st.spinner("Writing..."):
                result = call_backend(
                    "/cover-letter",
                    {"resume_text": resume_text, "job_description": job_description, "company_name": company_name},
                )
            if result:
                st.markdown(result)

elif feature == "Interview Question Generator":
    st.subheader("🎯 Interview Question Generator")
    resume_text, job_description = resume_and_jd_inputs(jd_required=True)
    if st.button("Generate Questions", type="primary"):
        if not resume_text.strip() or not job_description.strip():
            st.warning("Both resume and job description are required.")
        else:
            with st.spinner("Generating..."):
                result = call_backend("/interview-questions", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "Career Suggestions":
    st.subheader("🧭 Career Suggestions")
    resume_text, job_description = resume_and_jd_inputs()
    if st.button("Get Suggestions", type="primary"):
        if not resume_text.strip():
            st.warning("Paste a resume first.")
        else:
            with st.spinner("Thinking..."):
                result = call_backend("/career-suggestions", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)

elif feature == "ATS Score Explanation":
    st.subheader("⚡ ATS Score Explanation")
    resume_text, job_description = resume_and_jd_inputs()
    score = st.slider("Resume score (from your ATS tool)", 0, 100, 70)
    if st.button("Explain Score", type="primary"):
        if not resume_text.strip():
            st.warning("Paste a resume first.")
        else:
            with st.spinner("Explaining..."):
                result = call_backend(
                    "/ats-score-explanation",
                    {"resume_text": resume_text, "job_description": job_description, "score": score},
                )
            if result:
                st.markdown(result)

elif feature == "Final Summary":
    st.subheader("📝 Final Profile Summary")
    resume_text, job_description = resume_and_jd_inputs()
    if st.button("Summarize", type="primary"):
        if not resume_text.strip():
            st.warning("Paste a resume first.")
        else:
            with st.spinner("Summarizing..."):
                result = call_backend("/final-summary", {"resume_text": resume_text, "job_description": job_description})
            if result:
                st.markdown(result)
