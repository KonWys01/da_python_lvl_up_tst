from fastapi import FastAPI, Response, status
from fastapi import Request
import hashlib
import time
app = FastAPI()
app.counter = 0


@app.get('/')
def root():
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


"""
@app.get("/method")
def method():
    return {"method": "GET"}


@app.post("/method", status_code=201)
def method():
    return {"method": "POST"}


@app.delete("/method")
def method():
    return {"method": "DELETE"}


@app.put("/method")
def method():
    return {"method": "PUT"}


@app.options("/method")
def method():
    return {"method": "OPTIONS"}"""


@app.api_route("/method", methods=["GET", 'DELETE', 'PUT', 'OPTIONS'])
def method(request: Request):
    return {"method": request.method}


@app.post("/method", status_code=201)
def method(request: Request):
    return {"method": request.method}


@app.get("/auth/")
def auth(response: Response, password: str = "normal", password_hash: str = "hashed"):

    print(password)
    hashed = hashlib.sha512(password.encode())
    if hashed.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return response.status_code


