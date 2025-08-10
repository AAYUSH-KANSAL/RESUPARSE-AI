import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import matplotlib.pyplot as plt
import re
from io import BytesIO
from fpdf import FPDF
from agent import ATSResumeAgent

load_dotenv()

agent = ATSResumeAgent()

st.set_page_config(page_title="ResuParse AI ATS Analyzer", layout="wide", initial_sidebar_state="expanded")

# ----- Theme & Static Logo -----
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stButton>button { background-color: #0066cc; color: white; font-weight: bold; }
        .block-container {padding-top: 2rem;}
        .typing-effect span {
            display: inline-block;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
    </style>
""", unsafe_allow_html=True)

st.image("Jobwise_Logo.png", width=140)

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#00bfff;'>ResuParse AI</h1>
        <p style='font-size:18px;'>Your AI guide to get a job <span class='typing-effect'>💡</span></p>
    </div>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    return "".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join(para.text for para in doc.paragraphs)

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    for line in content.splitlines():
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode('latin1')

# -------- Sidebar Navigation --------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Tool", ["📄 Resume Analyzer", "✨ Magic Rephrase", "📁 ATS Templates", "📊 Skill Gap Analyzer"])

# -------- Resume Analyzer Tab --------
if page == "📄 Resume Analyzer":
    st.header("📄 ATS Resume Analyzer")
    st.markdown("### Upload Job Description or paste below")
    jd_file = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd_file")
    jd_text = st.text_area("Or paste the Job Description here")
    st.caption("📂 You can upload a job description file or paste it below.")
    jd = extract_text_from_pdf(jd_file) if jd_file and jd_file.name.lower().endswith("pdf") else extract_text_from_docx(jd_file) if jd_file else jd_text

    rc = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if rc and jd and st.button("🔍 Analyze Resume"):
        feedback = agent.analyze(rc, jd)
        if not feedback:
            st.error("No analysis response received.")
        elif isinstance(feedback, dict):
            st.markdown(feedback.get("summary", "No summary available."))
            match = re.search(r"(\d+)%", feedback.get("summary", ""))
            if match:
                perc = int(match.group(1))
                st.progress(perc)
                fig, ax = plt.subplots(figsize=(2, 2))
                ax.pie([perc, 100 - perc], labels=['Matched', 'Unmatched'],
                       autopct='%1.1f%%', startangle=90, colors=["#00bfff", "#333"])
                ax.axis('equal')
                st.pyplot(fig)
            st.download_button("📄 Download Feedback as PDF", data=generate_pdf(feedback.get("summary", "")), file_name="resume_feedback.pdf")
        else:
            st.markdown(feedback)

# -------- Magic Rephrase Tab --------
elif page == "✨ Magic Rephrase":
    st.header("🔮 Magic Rephrase")
    txt = st.text_area("Text to rephrase")
    if txt and st.button("Rephrase"):
        result = agent.rephrase(txt)
        st.success(result)

# -------- ATS Templates Tab --------
elif page == "📁 ATS Templates":
    st.header("📁 ATS Templates")
    st.markdown("Choose from these ATS-friendly resume templates:")
    templates = {
        "Modern Minimal": "https://docs.google.com/document/d/1NWFIz-EZ1ZztZSdXfrrcdffSzG-uermd/edit",
        "Elegant Blue": "https://docs.google.com/document/d/1xO7hvK-RQSb0mjXRn24ri3AiDrXx6qt8/edit",
        "Classic Chronological": "https://docs.google.com/document/d/1fAukvT0lWXns3VexbZjwXyCAZGw2YptO/edit"
    }
    for name, url in templates.items():
        st.markdown(f"**[{name}]({url})**")

# -------- Skill Gap Analyzer Tab --------
elif page == "📊 Skill Gap Analyzer":
    st.header("📊 Skill Gap Analyzer")
    st.markdown("### Upload Job Description or paste below")
    jd_file = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd_file2")
    jd_text = st.text_area("Or paste the Job Description here", key="jd2")
    st.caption("📂 You can upload a job description file or paste it below.")
    jd = extract_text_from_pdf(jd_file) if jd_file and jd_file.name.lower().endswith("pdf") else extract_text_from_docx(jd_file) if jd_file else jd_text

    rf2 = st.file_uploader("Upload resume", type=["pdf", "docx"], key="rf2")
    if rf2 and jd and st.button("Analyze Skill Gaps"):
        result = agent.skill_gap(rf2, jd)
        st.markdown(result)
