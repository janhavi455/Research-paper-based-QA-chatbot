# Research QA System V1

A system that allows users to upload research papers (PDFs) and ask natural language questions about their metadata using LLM-powered text-to-SQL.

## Architecture
User Uploads PDF → GROBID Extracts Metadata → SQLite Storage
↓
User Question → Llama 3 (Text-to-SQL) → SQL Query → Results → Llama 3 (Answer)

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **PDF Processing**: GROBID
- **Database**: SQLite
- **LLM**: Llama 3 via Ollama
- **Validation**: Pydantic 1.10.13
- **Python**: 3.12

## Prerequisites

1. **GROBID** - Running on http://localhost:8070
   ```bash
   # Download and start GROBID
   wget https://github.com/kermitt2/grobid/archive/0.7.3.zip
   unzip 0.7.3.zip
   cd grobid-0.7.3
   ./gradlew run

Ollama - Running with Llama 3
# Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull Llama 3 model
ollama pull llama3