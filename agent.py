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
            model_name="llama3-70b-8192",
            temperature=0.0  # Ensures deterministic output
        )

    def analyze(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        prompt = self._build_prompt(text, job_description)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return self._parse_response(response.content)

    def rephrase(self, text):
        prompt = f"""
        Rephrase the following resume content with ATS-optimized language, action verbs, and measurable impact:
{text}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def skill_gap(self, resume_file, job_description):
        text = self._extract_text(resume_file)
        prompt = f"""
        Compare the resume to the job description. Return:
        - Matched hard and soft skills
        - Missing hard and soft skills
        - Suggestions to close the skill gaps

        Resume:
{text[:6000]}

        Job Description:
{job_description[:2000]}
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

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
Analyze the resume below against the job description and return:
1. Match percentage
2. Missing keywords (hard + soft skills)
3. Final evaluation in 3 lines
4. 3–4 actionable improvement suggestions

Resume:
{resume_text[:6000]}

Job Description:
{job_description[:2000]}
        """

    def _parse_response(self, content):
        import json
        try:
            return json.loads(content)
        except:
            return {
                "summary": content.strip(),
                "strengths": [],
                "improvements": [],
                "keywords": [],
                "error": "Could not parse structured output."
            }
