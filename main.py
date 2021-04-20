from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/{method}")
def method_endpoint(method, response: Response):
    tmp = method.upper()
    if tmp == "GET" or "DELETE" or "OPTION" or "PUT":
        response.status_code = status.HTTP_200_OK
        return {"method": f"{method}".upper()}
    elif tmp == "POST":
        response.status_code = status.HTTP_201_CREATED
        return {"method": f"{method}".upper()}
    else:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return "Wrong method!"


