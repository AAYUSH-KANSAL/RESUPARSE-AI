# 🤖 ResuParse AI – The Ultimate AI Career Assistant

Transform your job search with the power of AI. **ResuParse AI** is a comprehensive career suite powered by **LLaMA 3** and **LangChain**, designed to optimize your resume, bridge skill gaps, and coach you through interviews and salary negotiations.

---

## 💎 Features

### 📄 1. AI Resume Analyzer
Get a match percentage, keyword analysis, and actionable improvement suggestions tailored to a specific Job Description (JD). Use a strict scoring matrix to see exactly how you compare to the ideal candidate.

### ✍️ 2. AI Cover Letter Architect
Generate highly persuasive, tailored cover letters that bridge your background with the company's needs. Focuses on impact and solving the employer's problems.

### 🎯 3. Skill Gap Bridge
Find exactly what's missing between your resume and the JD. Includes a **4-Week Career Roadmap** to help you systematically learn missing skills.

### 🛠️ 4. Resume-Builder Project Ideas
Address your skill gaps by building high-impact technical projects. Generates project titles, tech stacks, and even the exact **Resume Bullet Point** to use once you're done.

### 🎤 5. Interview Prep Master
Generate 10 customized interview questions (Behavioral & Technical) based on your profile. Includes "Why this?" rationale and "Pro Tips" for answering using the STAR method.

### 💰 6. Salary & Negotiation Coach
Estimate your market value in **INR** based on your seniority. Get ready-to-use negotiation scripts for scenarios like countering low offers or requesting bonuses.

---

## 🚀 How to Use

### 1. Set Up Environment
Get your Groq API key from [Groq Console](https://console.groq.com) and add it to a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Local Launch
```bash
# Clone the repository
git clone https://github.com/your-username/RESUPARSE-AI.git
cd RESUPARSE-AI

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🔧 Tech Stack
- **LLM**: LLaMA 3 (via Groq API)
- **Framework**: LangChain & Streamlit
- **PDF/Docx Parsing**: PyPDF2, python-docx
- **UI Architecture**: Glassmorphism with Custom CSS
- **PDF Export**: FPDF

---

## 🛡️ Privacy & Security
- **No Data Storage**: All processing happens live in your session.
- **Secure API Handling**: Keys are managed via `.env` and never exposed.
- **Premium UX**: Smooth transitions, interactive cards, and high-performance AI responses.

---

## 🎯 Target Audience
- **Job Seekers** looking for a competitive edge.
- **Students** building their first professional profile.
- **Career Switchers** needing specialized roadmaps.

---
*Built with ❤️ for ambitious professionals.*
