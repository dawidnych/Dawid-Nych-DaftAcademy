from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import date, datetime
import json
import hashlib

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return {"message": "Hello world!"}


@app.get("/auth")
def password_check(password: str, password_hash: str, response: Response):
    h = hashlib.sha512(password.encode('utf-8'))
    if h.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    elif password == "" or password_hash == "" or h.hexdigest() != password_hash:
        response.status_code = status.HTTP_401_UNAUTHORIZED
