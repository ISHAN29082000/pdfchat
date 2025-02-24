from fastapi import FastAPI, UploadFile
import fitz  # PyMuPDF for PDF processing

app = FastAPI()

pdf_text = ""  # Store extracted PDF text

@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    global pdf_text
    content = await file.read()

    # Save file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(content)

    # Extract text from PDF
    doc = fitz.open("temp.pdf")
    pdf_text = "\n".join([page.get_text("text") for page in doc])

    return {"message": "PDF Uploaded Successfully!"}

@app.get("/chat/")
async def chat(query: str):
    if not pdf_text:
        return {"response": "Please upload a PDF first."}

    # Simple text search
    matched_lines = [line for line in pdf_text.split("\n") if query.lower() in line.lower()]
    response = "\n".join(matched_lines[:5]) if matched_lines else "No relevant answer found."

    return {"response": response}
