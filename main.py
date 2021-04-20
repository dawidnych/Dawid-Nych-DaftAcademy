from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import date, datetime
import json
import hashlib

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return {"message": "Hello world!"}


@app.get("/{method}")
def method_endpoint(method: str, response: Response):
    lst = ["GET", "PUT", "OPTIONS", "DELETE"]
    if method.upper() in lst:
        response.status_code = status.HTTP_200_OK
        return {"method": f"{method}".upper()}
    elif method.upper() == "POST":
        response.status_code = status.HTTP_201_CREATED
        return {"method": f"{method}".upper()}
