import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv
genai.configure(api_key="Insert your API key here")

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text=''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text+=str(page.extract_text())
    return text

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracyss
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Extract text from PDF
        text = input_pdf_text(uploaded_file)
        # Generate input for Gemini model
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Parse the response string into a Python dictionary
        response_dict = eval(response)

        # Display the JD Match as a progress bar with percentage
        jd_match = int(response_dict["JD Match"].replace("%", ""))
        st.markdown("### JD Match Percentage")
        st.write(f"**{jd_match}%**")  # Display the percentage above the progress bar
        st.progress(jd_match / 100)  # Progress bar to show percentage match

        # Display missing keywords
        st.markdown("### Missing Keywords")
        missing_keywords = response_dict["MissingKeywords"]
        if missing_keywords:
            st.write(", ".join(missing_keywords))
        else:
            st.write("No missing keywords!")

        # Display Profile Summary
        st.markdown("### Profile Summary")
        st.markdown(f"**{response_dict['Profile Summary']}**")
