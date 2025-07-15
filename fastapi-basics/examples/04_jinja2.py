from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# FastAPI app
app = FastAPI()

# Mount static files (accessible via /static)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template loader
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "FastAPI + Jinja2 + Static Files",
            "items": ["FastAPI", "Jinja2", "StaticFiles", "Templates"],
        },
    )
