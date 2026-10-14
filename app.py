import streamlit as st
import requests

st.set_page_config(
    page_title = "AI Resume & Job Matcher",
    page_icon= "📄",
    layout = "centered"
)

st.title("AI Resume & Job Matcher")
st.write("Upload Your CV and Job Description is it suitable or Not!")

Upload_File = st.file_uploader("Upload Your PDF to this.", type=["pdf"])
job_description = st.text_area("Upload Your Job Description", height=200)

if st.button("Analyze Resume", type="primary"):
    if upload_file is not None and job_description.strip() != "":

        with st.spinner("Your resume is checking by AI. Wait a minute...")
            try:
                files = {"file": upload_File.name, upload_File.getvalue(), "application/pdf"}
                data = {"job_description": job_description}

                reponse = request.post("https://127.0.0.1:8000/analyze", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    st.success("Analyze successfully")

                    