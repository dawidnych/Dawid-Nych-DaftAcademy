from fastapi import FastAPI, Response, status, Request
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from typing import Optional
import hashlib

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return {"message": "Hello world!"}


# # 1.2
@app.api_route("/method", methods=["GET", "PUT", "OPTIONS", "DELETE", "POST"])
def method_endpoint(response: Response, request: Request):
    tmp = request.method
    lst = ["GET", "PUT", "OPTIONS", "DELETE"]
    if tmp in lst:
        response.status_code = status.HTTP_200_OK
        return {"method": f"{tmp}"}
    elif tmp == "POST":
        response.status_code = status.HTTP_201_CREATED
        return {"method": f"{tmp}"}


# #1.3
@app.get("/auth")
def password_check(password: Optional[str], password_hash: Optional[str], response: Response):
    h = hashlib.sha512(password.encode('utf-8'))
    if h.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    elif password == "" or password_hash == "" or h.hexdigest() != password_hash or password is None\
            or password_hash is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED


# 1.4
class RegisterIn(BaseModel):
    name: str
    surname: str


class RegisterOut(BaseModel):
    id: int
    name: str
    surname: str
    register_date: date
    vaccination_date: date

# Body request dla testu w Postmanie
user_data = {
    "name": "Jan",
    "surname": "Kowalski"
}

id = 0
my_dict = {}


@app.post("/register", response_model=RegisterOut, status_code=201)
def register_method(user: RegisterIn):
    global id
    id += 1
    delta = len(user.name) + len(user.surname)
    vacc_date = datetime.today() + timedelta(days=delta)

    x = RegisterOut(
        id=id, name=user.name, surname=user.surname,
        register_date=datetime.today().strftime('%Y-%m-%d'),
        vaccination_date=vacc_date.strftime('%Y-%m-%d')
    )

    my_dict[id] = x
    return x


#1.5
@app.get("/patient/{id}")
def get_patient_id(id: int, response: Response):
    if id < 1:
      response.status_code = status.HTTP_400_BAD_REQUEST
    elif id in my_dict.keys():
        response.status_code = status.HTTP_200_OK
        return my_dict[id]
    elif id not in my_dict.keys():
        response.status_code = status.HTTP_404_NOT_FOUND

