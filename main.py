from fastapi import FastAPI , Request , Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests
from fastapi.responses import FileResponse


app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates=Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})