import streamlit as st
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "backend"))


st.title("Research Paper based Q&A Chatbot")

backend_url = "http://127.0.0.1:8000"

# File uploader for PDFs
uploaded_files = st.file_uploader("Choose Research Papers (pdf)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
        files = []

        for file in uploaded_files:
            files.append(("pdfs", (file.name, file.getvalue(), "application/pdf")))
        with st.spinner("Uploading..."):
            try:
                
                response = requests.post(f"{backend_url}/upload_pdfs", files=files)

                if response.status_code != 200:
                    st.error("PDF upload disturbed.")
                    st.error(f"Error: {response.text}")
                else:
                    st.success("All files uploaded successfully")
                    st.json(response.json())
                    with st.spinner("Processing PDFs with GROBID..."):
                        grobid_response = requests.get(f"{backend_url}/process_pdfs_grobid")
                        if grobid_response.status_code == 200:

                            data = grobid_response.json()
                            metadata = data["metadata"]

                            st.success(f"GROBID processed {data['processed_count']} papers")
                            # Display metadata
                            for item in metadata:

                                with st.expander(f"📄 {item.get('filename','Paper')}"):

                                    st.write(f"**Title:** {item.get('title')}")
                                    st.write(f"**Authors:** {item.get('authors')}")
                                    st.write(f"**Journal:** {item.get('journal')}")
                                    st.write(f"**Year:** {item.get('year')}")
                                    st.write(f"**Abstract:** {item.get('abstract')}")

                        else:
                            st.error("GROBID processing failed")
                            st.error(grobid_response.text)

            except requests.exceptions.ConnectionError:
                st.error("❌ Connection failed - Is the backend server running? Make sure GROBID is also running on port 8070")
            except Exception as e:
                st.error("❌ An unexpected error occurred")
                st.write(str(e))
        

                    
                            
            