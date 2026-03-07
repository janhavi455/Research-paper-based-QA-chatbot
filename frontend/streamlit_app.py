import streamlit as st
import requests

st.title("Research Paper based Q&A Chatbot")

# File uploader for PDFs
uploaded_files = st.file_uploader("Choose Research Papers (pdf)", type=["pdf"], accept_multiple_files=True)

backend_url = "http://127.0.0.1:8000/upload_pdfs"
if uploaded_files:
        files = []

        for file in uploaded_files:
            files.append(("pdfs", (file.name, file.getvalue(), "application/pdf")))
        with st.spinner("Uploading..."):
            try:
                
                response = requests.post(backend_url, files=files)

                if response.status_code != 200:
                    st.error("PDF upload disturbed.")
                    st.error(f"Error: {response.text}")
                else:
                    st.success("All files uploaded successfully")
                    st.json(response.json())
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection failed - Is the backend server running?")
                
            except Exception as e:
                st.error("❌ An unexpected error occurred")
                st.write(str(e))