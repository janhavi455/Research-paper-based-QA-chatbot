import streamlit as st
from pathlib import Path

# Set up upload folder
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

st.title("Research Paper based Q&A Chatbot")

# File uploader for PDFs
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded PDF to uploads folder
    save_path = UPLOAD_FOLDER / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    st.write(f"Saved at: {save_path}")