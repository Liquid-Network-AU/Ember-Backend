from fastapi import FastAPI, File, UploadFile
import io
import PyPDF2
import numpy as np
import pinecone

# Set up Pinecone
pinecone.init(api_key="ba049302-4865-4a8d-9e96-bbc3174b480b", environment="us-central1-gcp")
#pinecone.create_index("pdf", dimension=512)

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Read uploaded PDF file as bytes
    pdf_bytes = await file.read()

    # Create an in-memory file object for PyPDF2
    pdf_file = io.BytesIO(pdf_bytes)

    # Create a PDF reader object using PyPDF2
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Extract text from the PDF
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Convert the text to a vector representation
    # (Note: This part depends on your specific use case and vectorization method)
    vector = np.random.rand(512)

    # Upload the vector to Pinecone
    pinecone_index = pinecone.Index(index_name="pdfs")
    pinecone_index.upsert(ids=[file.filename], vectors=[vector])

    return {"text": text}
