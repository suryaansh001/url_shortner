from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.db import insert_url, get_url
from app.utils import generate_short_code

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten")
async def convert_url_to_short_url(request: Request):
    data = await request.json()
    long_url = data.get("long_url")
    if not long_url:
        raise HTTPException(status_code=400, detail="Long URL is required")
    short_code = generate_short_code()
    insert_url(short_code, long_url)
    return JSONResponse({"short_code": short_code, "long_url": long_url})

@app.get("/{short_code}")
def redirect_to_long_using_short_code(short_code: str):
    long_url = get_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=long_url)