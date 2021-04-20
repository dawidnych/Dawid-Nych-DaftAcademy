from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import date

app = FastAPI()


class RegisterIn(BaseModel):
    name: str
    surname: str


class RegisterOut(BaseModel):
    id: int
    name: str
    surname: str
    register_date: date
    vaccination_date: date


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
    else:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return "Wrong method!"




# @app.post("/register")
# def register_method():
#     return

