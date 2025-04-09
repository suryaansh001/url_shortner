from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
import db,utils

load_dotenv()
app = FastAPI()
BASE_URL = os.getenv("DATABASE_URL")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/shorten")  
def convert_url_to_short_url(request: Request):
    long_url = request.json.get("long_url")
    if not long_url:
        raise HTTPException(status_code=400, detail="Long URL is required")
    short_code = utils.generate_short_code()
    db.insert_url(short_code, long_url)
    return {"short_code": short_code, "long_url": long_url}
@app.get("/{short_code}")
def redirect_to_long_using_short_code(short_code: str):
    
    if len(short_code) != 7:
        raise HTTPException(status_code=400, detail="Invalid short code")
    long_url = db.get_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=long_url)
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API!"}
