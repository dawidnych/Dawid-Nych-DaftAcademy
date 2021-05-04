import secrets

from fastapi import FastAPI, Response, Request, status, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime


app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
app.session_tokens = []
app.tokens = []


@app.get("/hello", response_class=HTMLResponse)
def hello_func(request: Request):
    return templates.TemplateResponse("task_3_1.html.j2", {
        "request": request, "date": datetime.today().strftime('%Y-%m-%d')})


@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        session_token = secrets.token_hex(16)
        app.session_tokens.insert(0, session_token)
        response.set_cookie(key="session_token", value=session_token)


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        token_value = secrets.token_hex(16)
        app.tokens.insert(0, token_value)
        return {"token": token_value}
