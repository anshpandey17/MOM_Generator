import google.generativeai as genai
import os
import streamlit as st
from docx import Document
from pypdf import PdfReader
from imageextractor import extract_text_image  # <-- keep your existing image extractor

# -------------------------
# Helper functions
# -------------------------
def text_extractor_pdf(file_obj):
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def text_extractor_docx(file_obj):
    docx_file = Document(file_obj)
    text = "\n".join([p.text for p in docx_file.paragraphs])
    return text

# -------------------------
# Configure the Model
# -------------------------
genai.configure(api_key="AIzaSyAd0ryPa58oDWVJOOlyck11oOPMHnJn2_A")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# Sidebar: File Upload
# -------------------------
user_text = None
st.sidebar.title(":orange[Upload your MoM Notes here:]")
st.sidebar.subheader("Only Upload Images, PDFs and DOCX")

user_file = st.sidebar.file_uploader(
    "Upload your file", 
    type=["pdf", "docx", "jpg", "jpeg", "png"]
)

if user_file:
    if user_file.type == "application/pdf":
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ["image/jpeg", "image/png"]:
        user_text = extract_text_image(user_file)
    else:
        st.error("Upload Correct File Format")

# -------------------------
# Main Page
# -------------------------
st.title(":blue[Minutes of Meeting]: :green[AI Assisted MoM generator in standardized form]")

tips = """ Tips to use this app:
* Upload your Notes in sidebar (Image, PDF or DOCX)
* Click on Generate MoM and get the standardized MoM """
st.write(tips)

if st.button("Generate MoM"):
    if user_text is None:
        st.error("Text is not generated")
    else:
        with st.spinner("Processing your data..."):
            prompt = f"""
            Assume you are an expert in creating Minutes of Meeting. 
            User has provided notes of a meeting in text format. Using this data, 
            create a standardized MoM for the user.

            Output must follow this structure:
            - Title : Title of Meeting
            - Heading : Meeting Agenda
            - Subheading : Name of Attendees (if not provided, use NA)
            - Subheading : Date of meeting and Place of meeting (if not provided, use Online)
            - Body :
              * Key points discussed
              * Decisions finalized
              * Actionable items
              * Additional notes
              * Deadlines discussed
              * Next meeting date (if any)
              * 2-3 lines summary

            Use bullet points and bold important keywords.

            The data provided by user is as follows:
            {user_text}
            """

            response = model.generate_content(prompt)

            st.write(response.text)

            st.download_button(
                label="Click to Download",
                data=response.text,
                file_name="MoM.txt",
                mime="text/plain"
            )
