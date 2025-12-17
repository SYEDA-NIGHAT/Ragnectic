from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from rag_chatbot import get_answer

app = FastAPI()

class Question(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>RAG Chatbot</title>

<style>
:root {
    --bg: #0f172a;
    --card: #020617;
    --user: #2563eb;
    --bot: #1e293b;
    --text: #e5e7eb;
    --muted: #94a3b8;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #020617, #0f172a);
    font-family: "Segoe UI", sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--text);
}

.chat-container {
    width: 420px;
    max-width: 95%;
    height: 600px;
    background: var(--card);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0,0,0,.6);
    overflow: hidden;
}

.header {
    padding: 18px;
    text-align: center;
    font-weight: 600;
    letter-spacing: 1px;
    background: rgba(255,255,255,0.03);
}

.messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.message {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    line-height: 1.5;
    animation: fadeIn .3s ease;
}

.user {
    background: var(--user);
    margin-left: auto;
    border-bottom-right-radius: 4px;
}

.bot {
    background: var(--bot);
    border-bottom-left-radius: 4px;
}

.input-area {
    display: flex;
    gap: 10px;
    padding: 15px;
    background: rgba(255,255,255,0.03);
}

input {
    flex: 1;
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 12px;
    color: var(--text);
    font-size: 15px;
}

input:focus {
    outline: none;
    border-color: var(--user);
}

button {
    background: var(--user);
    border: none;
    border-radius: 12px;
    padding: 0 18px;
    font-size: 16px;
    cursor: pointer;
    color: white;
}

button:hover {
    opacity: 0.9;
}

.typing {
    font-size: 14px;
    color: var(--muted);
    margin-bottom: 10px;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
</head>

<body>

<div class="chat-container">
    <div class="header">RAG CHATBOT</div>

    <div class="messages" id="messages">
        <div class="message bot">
            Hi 👋 Ask me anything from your documents.
        </div>
    </div>

    <div class="input-area">
        <input id="question" placeholder="Type your question..." />
        <button onclick="ask()">➤</button>
    </div>
</div>

<script>
async function ask() {
    const input = document.getElementById("question");
    const text = input.value.trim();
    if (!text) return;

    const messages = document.getElementById("messages");

    messages.innerHTML += `
        <div class="message user">${text}</div>
        <div class="typing" id="typing">Bot is typing...</div>
    `;
    messages.scrollTop = messages.scrollHeight;
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
    });

    const data = await res.json();
    document.getElementById("typing").remove();

    messages.innerHTML += `
        <div class="message bot">${data.answer}</div>
    `;
    messages.scrollTop = messages.scrollHeight;
}
</script>

</body>
</html>
"""

@app.post("/chat")
def chat(data: Question):
    return {"answer": get_answer(data.query)}
