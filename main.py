import os
from io import BytesIo
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv()

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title = "AI Resume & Job Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeAnalysis(BaseModel):
    match_score: int
    strength: List[str]
    missing_skills: List[str]
    summary_feedback: str

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text.strip()


@app.post("/analyze", response_model=ResumeAnalysis)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents)

        if not resume_text:
            raise HTTPException(status_code=400, detail="The uploaded PDF is empty or could not be read.")

        prompt = f"""
            You are an expert HR Manager and Technical Recruiter.
            Analyze the following resume text against the provided job description.
        
            Job Description:
            {job_description}
        
            Resume Text:
            {resume_text}
            """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeAnalysis,
            ),
        )

        import json
        result_dict = json.loads(response.text)
        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the resume: {str(e)}")

@app.get("/")
def home():
    return {"status": "Backend running fine!"}