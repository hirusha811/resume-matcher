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
                files = {"file": Upload_File.name, Upload_File.getvalue(), "application/pdf"}
                data = {"job_description": job_description}

                reponse = request.post("https://127.0.0.1:8000/analyze", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    st.success("Analyze successfully")

                    score = result.get("match_score", 0)
                    st.metric(label="Job Match Score", value=f"{score}%")

                    st.subheader("The Good Strenght in Resume")
                    for strength in result.get("strength", []):
                        st.write(f"- {strength}")
                    

                    st.subheader("Missing Skills")
                    for skill in result.get("missing_skills", []):
                        st.write(f"- {skills}")
                    
                    st.subheader("HR summary feedback")
                    st.write(result.get("ssummery_feedback", ""))
                
                else:
                    error_detail = response.json().get("detail", "Error")
                    st.error(f"Server Error: {error_detail}")
                
            except requests.exceptions.ConnectionError:
                st.error("Backend Server එකට සම්බන්ධ වීමට නොහැකි විය! කරුණාකර `uvicorn main:app --reload` command එක දීලා Backend එක Run කර ඇත්දැයි පරීක්ෂා කරන්න.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:

        st.warning("You have to upload both ones.")