from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "RAG chatbot is live 🚀"}

handler = Mangum(app)
