from fastapi import FastAPI, File, UploadFile
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logging.info("🚀 Server has started successfully!")

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_location = f"uploaded_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"✅ File '{file.filename}' uploaded successfully!")
        return {"filename": file.filename, "status": "uploaded", "location": file_location}

    except Exception as e:
        logging.error(f"❌ Error uploading file: {str(e)}")
        return {"error": "File upload failed"}

# Root endpoint to check if API is running
@app.get("/")
async def root():
    return {"message": "API is running successfully!"}
