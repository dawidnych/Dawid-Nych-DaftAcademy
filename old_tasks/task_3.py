import secrets

from fastapi import FastAPI, Response, Request, status, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime
from typing import Optional


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
        if len(app.session_tokens) < 3:
            app.session_tokens.append(session_token)
        else:
            del app.session_tokens[0]
            app.session_tokens.append(session_token)
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
        if len(app.tokens) < 3:
            app.tokens.append(token_value)
        else:
            del app.tokens[0]
            app.tokens.append(token_value)
        return {"token": token_value}


@app.get("/welcome_session")
def welcome_session(session_token: str = Cookie(None), format: Optional[str] = None):
    if session_token not in app.session_tokens or session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        if format is None:
            return PlainTextResponse(content="Welcome!", status_code=200)
        elif format.lower() == "json":
            json = {"message": "Welcome!"}
            return JSONResponse(content=json, status_code=200)
        elif format.lower() == "html":
            html_content = """
            <html>
            <head></head>
            <body>
                <h1>Welcome!</h1>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=200)
        else:
            return PlainTextResponse(content="Welcome!", status_code=200)


@app.get("/welcome_token")
def welcome_token(token: str, format: Optional[str] = None):
    if token not in app.tokens or token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        if format is None:
            return PlainTextResponse(content="Welcome!", status_code=200)
        elif format.lower() == "json":
            json = {"message": "Welcome!"}
            return JSONResponse(content=json, status_code=200)
        elif format.lower() == "html":
            html_content = """
                        <html>
                        <head></head>
                        <body>
                            <h1>Welcome!</h1>
                        </body>
                        </html>
                        """
            return HTMLResponse(content=html_content, status_code=200)
        else:
            return PlainTextResponse(content="Welcome!", status_code=200)


@app.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: Optional[str] = None):
    if session_token not in app.session_tokens or session_token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        app.session_tokens.remove(session_token)
        return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.delete("/logout_token")
def logout_token(token: str, format: Optional[str] = None):
    if token not in app.tokens or token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        app.tokens.remove(token)
        return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.get("/logged_out")
def logged_out(format: Optional[str] = None):
    if format is None:
        return PlainTextResponse(content="Logged out!", status_code=200)
    elif format.lower() == "json":
        json = {"message": "Logged out!"}
        return JSONResponse(content=json, status_code=200)
    elif format.lower() == "html":
        html_content = """
                    <html>
                    <head></head>
                    <body>
                        <h1>Logged out!</h1>
                    </body>
                    </html>
                    """
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)
