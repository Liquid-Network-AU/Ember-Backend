from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pinecone

app = FastAPI()

pinecone.init(api_key="YOUR_API_KEY", environment="us-west1-g")

class PineconeData(BaseModel):
    text: str
    filename: str

@app.post("/generate")
async def generate(data: PineconeData):
    try:
        pinecone_index = pinecone.Index(index_name=data.filename)
        embeddings = pinecone_index.embed([data.text])
        pinecone_index.upsert(ids=[data.filename], vectors=embeddings)
        return {"message": "PDF uploaded to Pinecone successfully"}
    except pinecone.exceptions.PineconeException as e:
        raise HTTPException(status_code=500, detail=str(e))