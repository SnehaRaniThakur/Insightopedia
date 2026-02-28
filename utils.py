# import os
# import pdfplumber
# from dotenv import load_dotenv
# from google import genai
# from PIL import Image
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
# from io import BytesIO
# import streamlit as st
# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     try:
#         api_key = st.secrets["GOOGLE_API_KEY"]
#     except Exception:
#         api_key = None

# if not api_key:
#     raise ValueError("GOOGLE_API_KEY not found.")

# client = genai.Client(api_key=api_key)

# def extract_text_from_pdf(upload_file, max_pages=60):
#     text = ""
#     with pdfplumber.open(upload_file) as pdf:
#         for i, page in enumerate(pdf.pages):
#             if i >= max_pages:
#                 break
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#     return text

# def extract_text_from_image(uploaded_file):
#     image = Image.open(uploaded_file)

#     response = client.models.generate_content(
#         model="models/gemini-2.5-flash",
#         contents=[
#             {
#                 "role": "user",
#                 "parts": [
#                     {"text": "Extract all readable text from this insurance document image clearly and accurately."},
#                     image
#                 ]
#             }
#         ]
#     )

#     if response.candidates:
#         return response.candidates[0].content.parts[0].text
#     return ""

# def generate_response(prompt):
#     try:
#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash",
#             contents=[
#                 {
#                     "role": "user",
#                     "parts": [{"text": prompt}]
#                 }
#             ]
#         )

#         if response.candidates:
#             return response.candidates[0].content.parts[0].text
#         return "AI returned empty response."

#     except Exception:
#         return "⚠️ AI service temporarily unavailable. Please try again later."


# def smart_trim(text, limit=12000):
#     if len(text) <= limit:
#         return text
#     part = limit // 3
#     return (
#         text[:part] +
#         text[len(text)//2 - part//2 : len(text)//2 + part//2] +
#         text[-part:]
#     )


# def generate_pdf(text):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = []

#     for line in text.split("\n"):
#         if line.strip():
#             elements.append(Paragraph(line, styles["Normal"]))
#             elements.append(Spacer(1, 8))

#     doc.build(elements)
#     buffer.seek(0)
#     return buffer



import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
import pdfplumber
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

# Load environment variables
load_dotenv()

# API Key Handling (Local + Cloud)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found.")

client = genai.Client(api_key=api_key)


# ---------------- PDF TEXT EXTRACTION ----------------
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


# ---------------- IMAGE TEXT EXTRACTION (Gemini Vision) ----------------
def extract_text_from_image(uploaded_file):
    image_bytes = uploaded_file.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "Extract all readable text from this insurance document image clearly and accurately.",
            genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_file.type,
            ),
        ],
    )

    return response.text if response.text else ""

# ---------------- LLM RESPONSE ----------------
def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        )

        if response.candidates:
            return response.candidates[0].content.parts[0].text
        return "AI returned empty response."

    except Exception:
        return "⚠️ AI service temporarily unavailable. Please try again later."


# ---------------- SMART TRIM ----------------
def smart_trim(text, limit=12000):
    if len(text) <= limit:
        return text
    part = limit // 3
    return (
        text[:part] +
        text[len(text)//2 - part//2 : len(text)//2 + part//2] +
        text[-part:]
    )


# ---------------- PDF GENERATION ----------------
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