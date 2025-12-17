from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# This tells FastAPI where your HTML and CSS are
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root(request: Request):
    # This serves your index.html from the /templates folder
    return templates.TemplateResponse("index.html", {"request": request})
