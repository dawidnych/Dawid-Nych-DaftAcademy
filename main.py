from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import date, datetime
import json
import hashlib

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return {"message": "Hello world!"}
