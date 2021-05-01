from fastapi import FastAPI, Response, status
from fastapi import Request
import hashlib
from datetime import date, timedelta
from pydantic import BaseModel
import pytest
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends


app = FastAPI()
security = HTTPBasic()
app.counter = 0


def number_of_letters(word):
    result = 0
    for character in word:
        if character.isalpha():
            result += 1
    return result


# Wykład 1, zadanie 1.1
@app.get('/')
def root():
    return {"message": "Hello world!"}


# Wykład 1
@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


# Wykład 1
@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


# Wyklad 1, zadanie 1.2 metoda na debila
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


# Wyklad 1, zadanie 1.2
@app.api_route("/method", methods=["GET", 'DELETE', 'PUT', 'OPTIONS'])
def method(request: Request):
    return {"method": request.method}


# Wyklad 1, zadanie 1.2 ciag dalszy
@app.post("/method", status_code=201)
def method(request: Request):
    return {"method": request.method}


# Wyklad 1, zadanie 1.3
@app.get("/auth")
def auth(response: Response, password: str = "", password_hash: str = ""):

    if len(password) == 0 or len(password_hash) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response.status_code
    hashed = hashlib.sha512(password.encode('utf-8'))
    if hashed.hexdigest() == password_hash:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response.status_code
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response.status_code


# Wyklad 1, zadanie 1.4
class Register(BaseModel):
    name: str
    surname: str


app.id_counter = 0
app.registration = dict()


@app.post("/register")
def register(response: Response, register_person: Register):
    register_date = date.today()
    days_to_add = number_of_letters(register_person.name) + number_of_letters(register_person.surname)
    vaccination_date = register_date + timedelta(days_to_add)

    app.id_counter += 1

    response.status_code = status.HTTP_201_CREATED
    data_of_person_to_be_registered = dict()
    data_of_person_to_be_registered["id"] = app.id_counter
    data_of_person_to_be_registered["name"] = register_person.name
    data_of_person_to_be_registered["surname"] = register_person.surname
    data_of_person_to_be_registered["register_date"] = register_date
    data_of_person_to_be_registered["vaccination_date"] = vaccination_date
    app.registration[app.id_counter] = data_of_person_to_be_registered

    return data_of_person_to_be_registered


# Wyklad 1, zadanie 1.5
@app.get("/patient/{id}")
def patient(response: Response, id: int):
    if id > app.id_counter:  # nie ma takiego pacjenta
        response.status_code = status.HTTP_404_NOT_FOUND
        return response.status_code
    elif id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code

    return app.registration[id]


# Wyklad 2, zadanie 2.1
def greetings(callable):
    def inner(*args):
        val = callable(*args)
        val = val.lower()
        result = ""
        for word in val.split():
            result += word.capitalize()
            result += " "
        result = result[:-1]
        result = "Hello " + result
        val = result
        return result
    return inner


# rozwiazanie pawła
"""def greetings(callable):
    def inner(*args):
        Iname = callable(*args).title()
        return "Hello" + Iname
    return inner"""


@greetings
def name_surname(name):
    return name


print("result=")
name_surname("joe doe")
print(name_surname("joe doe"))


# Wyklad 2, zadanie 2.2
def is_palindrome(callable):
    def inner(*args):
        val = callable(*args)
        original_name = val
        original_name = original_name.lower()
        result = ""
        for character in original_name:
            if character.isalpha() or character.isnumeric():
                result += character
        if result == result[::-1]:
            return str(val + " - is palindrome")
        else:
            return str(val + " - is not palindrome")
    return inner


@is_palindrome
def sentence():
    return "1111111111011111111111"


sentence()
print()


# Wyklad 2, zadanie 2.3
def format_output(*args):
    list_of_arguments_double_floor = list(args)

    def decorator(value_func):
        def wrapper():  # w rozwiazaniu na stronie def wrapper(*args):
            value = value_func()  # w rozwiazaniu na stronie value = value_func(args)
            updated_keys_and_values = dict()

            for element in list_of_arguments_double_floor:
                updated_keys_and_values[element] = ''

            for key in updated_keys_and_values.keys():
                if '__' in key:  # ten klucz zawiera wiecej niz 1 klucz i trzeba rozdzielic
                    for key_splitted in key.split('__'):
                        if key_splitted in value.keys():
                            updated_keys_and_values[key] += value[key_splitted]
                            updated_keys_and_values[key] += ' '
                        else:
                            raise ValueError
                    updated_keys_and_values[key] = updated_keys_and_values[key][:-1]  # usuwanie spacji w po ostatnim slowie
                elif key in value.keys():
                    updated_keys_and_values[key] += value[key]
                else:
                    raise ValueError
            return updated_keys_and_values

        return wrapper
    return decorator


@format_output("first_name", "age")
def show_dict():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa",
    }

print("only 1 wrapper")
# print(show_dict())
with pytest.raises(ValueError):
    show_dict()


# Wyklad 2, zadanie 2.4 a)
class ExampleClass:
    pass


def add_class_method(ExampleClass):
    def wrapper(function):
        setattr(ExampleClass, function.__name__, function)
        return function
    return wrapper


@add_class_method(ExampleClass)
def foo():
    return "siemanko"


# ExampleClass.foo()
# foo()


# Wyklad 2, zadanie 2.4 b)
def add_instance_method(ExampleClass):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(ExampleClass, func.__name__, wrapper)
        return func
    return decorator


@add_instance_method(ExampleClass)
def bar():
    return "Hello again!"


# wywołanie funkcji bar dla obiektu klasy ExampleClass
# a = ExampleClass()
# a.bar()


@app.get('/hello', response_class=HTMLResponse)
def hello():
    return f"""
        <html>
            <head>
                <title>have no idea whether it works</title>
            </head>
            <body>
                <h1>Hello! Today date is 2021-04-30</h1>
            </body>
        </html>
        """


token_login_session = "session"
token_login_token = "token"
import http.cookies


@app.post("/login_session", status_code=201)
def read_current_user(resposne: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        resposne.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        resposne.set_cookie(key="session_token", value="siemanko-jedzonko")
        global token_login_session
        token_login_session = "siemanko-jedzonko"
        return resposne


@app.post("/login_token", status_code=201)
def read_current_user(resposne: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        resposne.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        token_value = "dwa"
        global token_login_token
        token_login_token = token_value
        return {"token": token_value}

