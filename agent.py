import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

load_dotenv()

class ATSResumeAgent:
    def __init__(self, groq_api_key=None):
        self.llm = ChatGroq(
            api_key=groq_api_key or os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-20b",
            temperature=0.0  # Ensures deterministic output
        )

    def analyze_text(self, text, job_description):
        prompt = self._build_prompt(text, job_description)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._parse_response(response.content)

    def analyze(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        return self.analyze_text(text, job_description)

    def rephrase(self, text):
        prompt = f"""
        Rephrase the following resume content with ATS-optimized language, action verbs, and measurable impact:
{text}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def skill_gap_text(self, text, job_description):
        prompt = f"""
        Analyze the resume against the job description and identify skill gaps.
        Return the response EXCLUSIVELY in JSON format with the following keys:
        - "missing_skills": A list of specific hard/soft skills missing.
        - "matched_skills": A list of skills that match.
        - "bridge_the_gap": A list of objects, each with:
            - "skill": Name of the missing skill.
            - "advice": Brief strategy to learn it.
            - "resources": A list of 2-3 specific resource names (e.g. "Coursera: Python for Data Science", "YouTube: Advanced React Patterns").
        - "timeline": A suggested 2-4 week learning roadmap.

        Resume:
{text}

        Job Description:
{job_description}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._parse_json_or_fallback(response.content)

    def _parse_json_or_fallback(self, content):
        import json
        import re
        try:
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if match:
                content = match.group(1)
            return json.loads(content)
        except:
            return {"error": "Failed to parse JSON", "raw_content": content}

    def skill_gap(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        return self.skill_gap_text(text, job_description)

    def generate_cover_letter_text(self, text, job_description):
        prompt = f"""
        Act as an expert career coach. Write a highly tailored, persuasive cover letter.
        Focus on:
        - A powerful opening hook mentioning the specific company (placeholder: [Company Name]).
        - Bridging the gap: Explain how the candidate's achievements (from Resume) directly solve the problems mentioned in the Job Description.
        - Keep it concise, professional, and confident.
        - Output the raw text of the letter without any introductory or concluding AI chatter.

        Resume:
{text}

        Job Description:
{job_description}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
        
    def generate_cover_letter(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        return self.generate_cover_letter_text(text, job_description)

    def generate_interview_questions_text(self, text, job_description):
        prompt = f"""
        Act as a Senior Lead Interviewer.
        Based on the Resume and JD, generate 10 impactful interview questions.
        Provide the response EXCLUSIVELY in JSON format with a list of objects under the key "questions".
        Each object should have:
        - "category": "Behavioral" or "Technical".
        - "question": The interview question.
        - "why": The logic behind asking this (what are you testing?).
        - "star_tip": A short advice on how to answer using the STAR method or technical keys.

        Resume:
{text}

        Job Description:
{job_description}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._parse_json_or_fallback(response.content)

    def generate_interview_questions(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        return self.generate_interview_questions_text(text, job_description)

    def _extract_text(self, file):
        if file.name.lower().endswith(".pdf"):
            reader = PdfReader(file)
            return " ".join([p.extract_text() or "" for p in reader.pages])
        elif file.name.lower().endswith(".docx"):
            doc = Document(file)
            return " ".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format")

    def _build_prompt(self, resume_text, job_description):
        return f"""
You are an ATS (Applicant Tracking System) Resume Evaluator.
Analyze the resume below against the job description and return your response EXCLUSIVELY in valid JSON format.
You must use a **STRICT JD-BIASED SCORING MATRIX**. The comparison must be unforgiving; if the candidate lacks core skills or industry context from the JD, the score must reflect that gap heavily.

**Scoring Weights:**
1. **Keyword & Skill Precision (50%)**: Direct match of hard skills, tools, and technical competencies.
2. **Role & Industry Alignment (25%)**: Prior experience in the exact same or very similar role/industry. Irrelevant experience should be scored low.
3. **Direct Requirement Satisfaction (15%)**: Degrees, certifications, and "Must-have" qualifications.
4. **General Execution (10%)**: Professionalism and impact verbs (secondary to technical fit).

Return the following keys:
- "overall_match": An integer between 0 and 100 representing the total match score.
- "summary": A final evaluation in 3 lines, explaining why the resume does or does not meet the specific JD requirements.
- "category_scores": A nested JSON object with keys "keyword_match", "industry_fit", "requirements", "execution" (each 0-100).
- "matched_keywords": A list of hard and soft skills found.
- "missing_keywords": A list of missing hard and soft skills.
- "improvements": A list of 3-4 actionable improvement suggestions.

Resume:
{resume_text}

Job Description:
{job_description}
        """

    def _parse_response(self, content):
        import json
        import re
        try:
            # Try to extract JSON if it is inside markdown code blocks
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if match:
                content = match.group(1)
            return json.loads(content)
        except:
            return {
                "overall_match": 50,
                "summary": content.strip()[:150] + "...",
                "category_scores": {"keyword_match": 50, "industry_fit": 50, "requirements": 50, "execution": 50},
                "strengths": [],
                "matched_keywords": [],
                "missing_keywords": ["JSON Parse Error"],
                "improvements": ["Failed to extract structured response from LLaMA model."],
                "error": "Could not parse structured output."
            }
