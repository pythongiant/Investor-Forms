import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
client = OpenAI(api_key=st.secrets['api_key'])

def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

st.title("HUBX Form Transcriber")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Extracting text from the uploaded PDF...")
    pdf_text = extract_text_from_pdf(uploaded_file)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature = 0.2,
        messages=[{"role":"system","content":"""
        Make a form out of this document. Reply only with HTML. Use these HTML fields as required:

        Text-based fields

Single-line text input: <input type="text">
Multi-line text input (textarea): <textarea>
Email input: <input type="email">
URL input: <input type="url">
Telephone input: <input type="tel">
Password input: <input type="password">
Numeric fields

Integer input: <input type="number">
Decimal input: <input type="number" step="0.01">
Range input (slider): <input type="range">
Selection fields

Checkbox: <input type="checkbox">
Radio button: <input type="radio">
Dropdown select: <select>
Multiselect: <select multiple>
Date and time fields

Date input: <input type="date">
Time input: <input type="time">
DateTime input: <input type="datetime-local">
File and image fields

File input: <input type="file">
Image input: <input type="image">
Other fields

Hidden input: <input type="hidden">
Button: <input type="button"> or <button>
Submit button: <input type="submit">
Reset button: <input type="reset">
Specialized fields

Color input: <input type="color">
Search input: <input type="search">

        """},{
            "role":"user",
            "content":pdf_text
        }]
    )
    st.write("Here is the transcribed text:")
    st.html(response.choices[0].message.content)
    st.text_area("Transcribed Text", pdf_text, height=500)
else:
    st.write("Please upload a PDF file to transcribe its contents.")
