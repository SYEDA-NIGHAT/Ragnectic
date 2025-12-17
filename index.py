from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "RAG chatbot is live 🚀"}
