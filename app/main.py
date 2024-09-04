from fastapi import FastAPI, Request, Depends
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app import models
from app import schemas
from app import utility
import threading
from app.database import get_db
from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind= engine)

app = FastAPI()

templating = Jinja2Templates(directory="/home/hasib/Projects/FastAPI/OpenAI-Content/templates")


@app.get('/', response_class= HTMLResponse)
@app.get('/sentiment', response_class=HTMLResponse)
def read_root(request : Request):
    return  templating.TemplateResponse("index.html", {"request": request})


@app.post('/generate/')
async def generate_content(payload : schemas.GeneratePayload , db :  Session = Depends (get_db)):
    generated_text  = await run_in_threadpool(utility.generate_content, db, payload.topic)
    return {generated_text : generated_text}
    