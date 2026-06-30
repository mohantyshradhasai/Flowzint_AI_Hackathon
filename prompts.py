"""
Prompt templates for the AI Career Copilot.

Each function takes the relevant fields and returns a single prompt string
ready to send to the Cohere chat API.
"""


def resume_feedback_prompt(resume_text: str, job_description: str = "") -> str:
    return f"""You are an expert career coach and ATS system.

Analyze the following resume and provide detailed, constructive feedback.

Focus on:
- Clarity and structure
- ATS optimization (keywords, formatting)
- Impact of bullet points
- Skills relevance
- Missing sections or improvements

Resume:
{resume_text}

Job Description (if available):
{job_description}

Output format:
1. Overall Score (out of 100)
2. Strengths (bullet points)
3. Weaknesses (bullet points)
4. Section-wise feedback (Skills, Projects, Experience, Education)
5. Final actionable suggestions

Keep feedback specific, professional, and actionable. Avoid generic statements."""


def skill_gap_prompt(resume_text: str, job_description: str) -> str:
    return f"""You are an AI recruitment assistant.

Compare the resume with the job description and identify skill gaps.

Resume:
{resume_text}

Job Description:
{job_description}

Output:
1. Matching Skills
2. Missing Skills (VERY IMPORTANT)
3. Partially Matching Skills
4. Recommended Skills to Learn (prioritized)
5. Final summary in 2-3 lines

Be precise and avoid repetition."""


def bullet_rewriter_prompt(bullet_points: str, job_description: str = "") -> str:
    return f"""You are an expert resume writer.

Rewrite the following resume bullet points to make them:
- More impactful
- Quantified (ONLY add a metric if it is implied by the original text or
  reasonably inferable; otherwise insert a clearly marked placeholder like
  [ADD METRIC] rather than inventing a number)
- ATS-friendly
- Action-oriented

Original Bullet Points:
{bullet_points}

Job Description:
{job_description}

Output:
- Improved bullet points only (no explanation)
- Use strong action verbs
- Add measurable impact where possible, never fabricated"""


def full_resume_improver_prompt(resume_text: str, job_description: str = "") -> str:
    return f"""You are a professional resume editor.

Improve the entire resume to:
- Increase ATS compatibility
- Enhance clarity and readability
- Add impact and quantification (do not invent metrics that aren't implied
  by the original content; use [ADD METRIC] placeholders if needed)
- Align with the job description

Resume:
{resume_text}

Job Description:
{job_description}

Output:
- Fully improved resume
- Maintain structure (do not remove sections)
- Improve wording and formatting
- Keep it concise and professional"""


def cover_letter_prompt(resume_text: str, job_description: str, company_name: str = "") -> str:
    company_line = f"Company Name: {company_name}\n" if company_name else ""
    return f"""You are a professional career assistant.

Generate a personalized cover letter based on the resume and job description.

Resume:
{resume_text}

Job Description:
{job_description}
{company_line}
Output:
- Professional cover letter (200-300 words)
- Strong opening paragraph
- Highlight relevant skills and experience
- Align with job role
- End with confident closing
- If no company name is given, address it generically without inventing one

Tone: Professional, confident, and enthusiastic."""


def interview_questions_prompt(resume_text: str, job_description: str) -> str:
    return f"""You are a technical interviewer.

Generate interview questions based on the candidate's resume and job description.

Resume:
{resume_text}

Job Description:
{job_description}

Output:
1. 5 Technical Questions
2. 3 Project-based Questions
3. 3 Behavioral Questions
4. 2 HR Questions

Questions should be relevant, realistic, and role-specific."""


def career_suggestions_prompt(resume_text: str, job_description: str = "") -> str:
    return f"""You are a career advisor.

Based on the resume and skill gaps, suggest improvements.

Resume:
{resume_text}

Job Description:
{job_description}

Output:
1. Top 5 skills to learn
2. Suggested projects to build
3. Recommended certifications
4. Career improvement roadmap (short)

Keep suggestions practical and achievable."""


def ats_score_explanation_prompt(resume_text: str, job_description: str, score: int) -> str:
    return f"""You are an ATS system.

Explain the resume score in a clear and structured way.

Resume Score: {score}
Resume:
{resume_text}

Job Description:
{job_description}

Output:
1. Why this score was given
2. Key missing keywords
3. Formatting issues (if any)
4. How to improve score

Keep explanation simple and user-friendly."""


def final_summary_prompt(resume_text: str, job_description: str = "") -> str:
    return f"""You are an AI assistant.

Provide a concise summary of the candidate's profile.

Resume:
{resume_text}

Job Description:
{job_description}

Output:
- 3-4 line professional summary
- Highlight strengths
- Mention improvement areas briefly

Keep it short and impactful."""
