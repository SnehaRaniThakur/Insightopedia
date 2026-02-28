import os
import pdfplumber
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
import streamlit as st
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found.")

genai.configure(api_key=api_key)

def extract_text_from_pdf(upload_file, max_pages=60):
    text = ""
    with pdfplumber.open(upload_file) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= max_pages:
                break
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "AI returned empty response."

    except Exception:
        return "⚠️ AI service temporarily unavailable. Please try again later."

def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "AI returned empty response."

    except Exception:
        return "⚠️ AI service temporarily unavailable. Please try again later."



def smart_trim(text, limit=12000):
    if len(text) <= limit:
        return text
    part = limit // 3
    return (
        text[:part] +
        text[len(text)//2 - part//2 : len(text)//2 + part//2] +
        text[-part:]
    )


def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    for line in text.split("\n"):
        if line.strip():
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)
    return buffer