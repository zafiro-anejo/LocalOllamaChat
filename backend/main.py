import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import config
from pdf_processor import process_document
from engine import RAGEngine

os.makedirs(config.INITIAL_FILES_DIR, exist_ok=True)
os.makedirs(config.PROCESSED_FILES_DIR, exist_ok=True)

pdf_files = list(config.INITIAL_FILES_DIR.glob("*.pdf"))
if not pdf_files:
    print(f"[WARNING] No PDF files in {config.INITIAL_FILES_DIR}")
else:
    print(f"Found {len(pdf_files)} PDF files. Converting...")
    for pdf_path in pdf_files:
        md_filename = pdf_path.stem + ".md"
        md_path = config.PROCESSED_FILES_DIR / md_filename
        markdown_content = process_document(str(pdf_path))
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
    print("Conversion completed.")

print("Initializing RAGEngine and building index...")
rag = RAGEngine(source_dir=config.PROCESSED_FILES_DIR, rebuild_if_exists=True)

app = FastAPI(title="RAG Chatbot API")

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"response": f"[ERROR] {type(exc).__name__}"}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    answer = rag.ask(request.message)
    return QueryResponse(response=answer)