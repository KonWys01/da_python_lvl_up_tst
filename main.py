from fastapi import FastAPI, Response, status, Cookie, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi import HTTPException
import random
import string
import hashlib
from datetime import date, timedelta
from pydantic import BaseModel
import pytest

import aiosqlite

app = FastAPI()
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


# Wyklad 3, zadanie 3.1
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


# Wyklad 3, zadanie 3.2
def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(30))
    return result_str


security = HTTPBasic()
app.secret_key = "aidbskgbdklgbnsdkgjbdgkjdbgfkd"
app.login_session_tokens = []
app.login_token_tokens = []
token_login_session = "session"
token_login_token = "token"


@app.post("/login_session")
def read_current_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if len(user) == 0 or len(password) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    if user != "4dm1n" or password != "NotSoSecurePa$$":
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        session_token = get_random_string()
        # maksymalnie 3 użytkowników
        if len(app.login_session_tokens) == 3:
            app.login_session_tokens.pop(0)
        app.login_session_tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        response.status_code = status.HTTP_201_CREATED
        return response


@app.post("/login_token")
def read_current_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if len(user) == 0 or len(password) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    if user != "4dm1n" or password != "NotSoSecurePa$$":
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        response.status_code = status.HTTP_201_CREATED
        token_value = get_random_string()
        # maksymalnie 3 użytkowników
        if len(app.login_token_tokens) == 3:
            app.login_token_tokens.pop(0)

        app.login_token_tokens.append(token_value)
        return {"token": token_value}


# Wyklad 3, zadanie 3.3
@app.get("/welcome_session")
def welcome_session(*, response: Response, session_token: str = Cookie(None), format: str = ""):
    if session_token not in app.login_session_tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    else:
        response.status_code = status.HTTP_200_OK
        if format == "":
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)
        elif format == "json":
            result = {"message": "Welcome!"}
            return JSONResponse(content=result, status_code=200)
        elif format == "html":
            html = f"""
                    <html>
                        <head>
                            <title>have no idea whether it works</title>
                        </head>
                        <body>
                            <h1>Welcome!</h1>
                        </body>
                    </html>
                    """
            return HTMLResponse(content=html, status_code=200)
        else:
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)


@app.get("/welcome_token")
def welcome_token(response: Response, token: str = "", format: str = ""):
    if token not in app.login_token_tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    else:
        response.status_code = status.HTTP_200_OK
        if format == "":
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)
        elif format == "json":
            result = {"message": "Welcome!"}
            return JSONResponse(content=result, status_code=200)
        elif format == "html":
            html= f"""
                    <html>
                        <head>
                            <title>have no idea whether it works</title>
                        </head>
                        <body>
                            <h1>Welcome!</h1>
                        </body>
                    </html>
                    """
            return HTMLResponse(content=html, status_code=200)
        else:
            result = "Welcome!"
            return PlainTextResponse(content=result, status_code=200)


# Wyklad 3, zadanie 3.4 oraz 3.5(usprawnienia)
@app.delete("/logout_session")
def logout_session(*, response: Response, session_token: str = Cookie(None), format: str = ""):
    if session_token not in app.login_session_tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        for i in range(len(app.login_session_tokens)):
            if app.login_session_tokens[i] == session_token:
                app.login_session_tokens.pop(i)
                break
        response.status_code = status.HTTP_302_FOUND
        return RedirectResponse(f"https://da-first-homework-2021.herokuapp.com/logged_out?token={session_token}&format={format}"
                                , status_code=303)


@app.delete("/logout_token")
def logout_session(response: Response, token: str = "", format: str = ""):
    if token not in app.login_token_tokens:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        for i in range(len(app.login_token_tokens)):
            if app.login_token_tokens[i] == token:
                app.login_token_tokens.pop(i)
                break
        response.status_code = status.HTTP_302_FOUND
        return RedirectResponse(f"https://da-first-homework-2021.herokuapp.com/logged_out?token={token}&format={format}"
                                ,status_code=303)


@app.get("/logged_out")
def logged_out(response: Response, format: str = ""):
    if format == "":
        result = "Logged out!"
        return PlainTextResponse(content=result, status_code=200)
    elif format == "json":
        result = {"message": "Logged out!"}
        return JSONResponse(content=result, status_code=200)
    elif format == "html":
        html = f"""
                <html>
                    <body>
                        <h1>Logged out!</h1>
                    </body>
                </html>
                """
        return HTMLResponse(content=html, status_code=200)
    else:
        result = "Logged out!"
        return PlainTextResponse(content=result, status_code=200)


# Wyklad 4
@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific



@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()


# Wyklad 4, zadanie 4.1
@app.get("/categories")
async def categories(response: Response):
    response.status_code = status.HTTP_200_OK
    app.db_connection.row_factory = aiosqlite.Row
    cursor = await app.db_connection.execute(
        """
        SELECT CategoryID AS "id", CategoryName AS "name" FROM Categories ORDER BY CategoryID
        """)
    data = await cursor.fetchall()
    return {
        "categories": data
    }


@app.get("/customers")
async def customers(response: Response):
    response.status_code = status.HTTP_200_OK
    app.db_connection.row_factory = aiosqlite.Row
    # COALESCE zamienia nulla na pusty string
    cursor = await app.db_connection.execute(
        """
        SELECT CustomerID AS "id", CompanyName AS "name", 
        COALESCE(Address, '') || " " || COALESCE(PostalCode, '') || " " || COALESCE(City, '') || " " || COALESCE(Country, '') AS "full_address"
        FROM Customers
        ORDER BY UPPER(CustomerID);
        """)
    data = await cursor.fetchall()
    return {"customers": data}


# Wyklad 4, zadanie 4.2
@app.get("/products/{id}")
async def products(response: Response, id: int):
    # znajdowanie najwiekszego id

    cursor = await app.db_connection.execute(f"SELECT ProductID FROM Products ORDER BY ProductID DESC")
    data = await cursor.fetchall()
    max_id = data[0][0]

    if id < 1 or id > max_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    cursor = await app.db_connection.execute("SELECT ProductID, ProductName FROM Products WHERE ProductID=:id", {'id': id})
    data = await cursor.fetchone()
    response.status_code = status.HTTP_200_OK
    return {"id": data[0], "name": data[1]}


# Wyklad 4, zadanie 4.3
@app.get("/employees")
async def employees(response: Response, limit: int = 100, offset: int = 0, order: str = "EmployeeID"):
    app.db_connection.row_factory = aiosqlite.Row
    if order == 'EmployeeID':
        result = True
    elif order != 'first_name' and order != 'last_name' and order != 'city':
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    if order == 'first_name':
        order = 'FirstName'
    elif order == 'last_name':
        order = 'LastName'
    elif order == 'city':
        order = 'City'
    cursor = await app.db_connection.execute(
        f"""
        SELECT EmployeeID AS id, FirstName AS first_name, LastName AS last_name, City AS city 
        FROM Employees
        ORDER BY UPPER ({order})
        LIMIT {limit}
        OFFSET ({offset});
        """)
    data = await cursor.fetchall()
    return {"employees": data}


# Wyklad 4, zadanie 4.4
@app.get("/products_extended")
async def employees(response: Response):
    app.db_connection.row_factory = aiosqlite.Row
    cursor = await app.db_connection.execute(
        f"""
            SELECT Products.ProductID AS id, Products.ProductName AS name, Categories.CategoryName AS category, Suppliers.CompanyName AS supplier 
            FROM Products, Categories, Suppliers
            WHERE Products.CategoryID = Categories.CategoryID and Products.SupplierID = Suppliers.SupplierID
            ORDER BY Products.ProductID
            """)
    data = await cursor.fetchall()
    return {"products_extended": data}


# Wyklad 4, zadanie 4.5
@app.get("/products/{id}/orders")
async def orders(response: Response, id: int):

    app.db_connection.row_factory = aiosqlite.Row

    cursor = await app.db_connection.execute(
        f"""
            SELECT Orders.OrderID AS id, Customers.CompanyName AS customer, [Order Details].Quantity AS quantity,
            ([Order Details].UnitPrice * [Order Details].Quantity) - ([Order Details].Discount * ([Order Details].UnitPrice * [Order Details].Quantity)) AS total_price
            FROM Orders, Customers, [Order Details]
            WHERE Orders.CustomerID = Customers.CustomerID and Orders.OrderID = [Order Details].OrderID
            ORDER BY (Orders.OrderID) DESC  
            LIMIT 1
            """)
    data = await cursor.fetchall()
    max_id = data[0]['id']

    cursor = await app.db_connection.execute(
        f"""
            SELECT Orders.OrderID AS id, Customers.CompanyName AS customer, [Order Details].Quantity AS quantity,
            ([Order Details].UnitPrice * [Order Details].Quantity) - ([Order Details].Discount * ([Order Details].UnitPrice * [Order Details].Quantity)) AS total_price
            FROM Orders, Customers, [Order Details]
            WHERE Orders.CustomerID = Customers.CustomerID and Orders.OrderID = [Order Details].OrderID
            ORDER BY (Orders.OrderID)  
            LIMIT 1
            """)
    data = await cursor.fetchall()
    min_id = data[0]['id']

    if max_id >= id >= min_id:
        response.status_code = status.HTTP_200_OK
        cursor = await app.db_connection.execute(
            f"""
                SELECT Orders.OrderID AS id, Customers.CompanyName AS customer, [Order Details].Quantity AS quantity,
                ROUND(([Order Details].UnitPrice * [Order Details].Quantity) - ([Order Details].Discount * ([Order Details].UnitPrice * [Order Details].Quantity)),2) AS total_price
                FROM Orders, Customers, [Order Details]
                WHERE Orders.CustomerID = Customers.CustomerID and Orders.OrderID = [Order Details].OrderID and Orders.OrderID = :id
                GROUP BY Orders.OrderID
                """, {'id': id})
        data = await cursor.fetchall()
        return {"orders": data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response


# Wyklad 4, zadanie 4.6
class Categories(BaseModel):
    name: str


@app.post("/categories")
async def categories_6(response: Response, category: Categories):
    app.db_connection.row_factory = aiosqlite.Row
    cursor = await app.db_connection.execute(
        f"""
            INSERT INTO Categories (CategoryName)
            VALUES(:category_name)
            """, {'category_name': category.name})
    data = await cursor.fetchall()

    cursor = await app.db_connection.execute(
        f"""
           Select CategoryID as id, CategoryName as name
           from Categories 
           Order by CategoryID DESC
           limit 1
        """)
    data = await cursor.fetchall()
    response.status_code = status.HTTP_201_CREATED
    return data[0]


class CategoriesID(BaseModel):
    name: str


@app.put("/categories/{id}")
async def categories_6(response: Response, id: int,  category: CategoriesID):
    app.db_connection.row_factory = aiosqlite.Row

    cursor = await app.db_connection.execute(
    """
    SELECT EXISTS(SELECT 1 FROM Categories WHERE CategoryID=:id) as if_exist
    """, {'id': id})
    data = await cursor.fetchall()
    if_exist = data[0]['if_exist']
    if if_exist == 1:
        cursor = await app.db_connection.execute(
            f"""
               update Categories
               set CategoryName = :name
               where CategoryID = :id
            """, {'name': category.name, "id": id})
        data = await cursor.fetchall()

        cursor = await app.db_connection.execute(
            f"""
                select CategoryID as id, CategoryName as name
                from Categories
                where CategoryID = :id
            """, {"id": id})
        data = await cursor.fetchall()

        response.status_code = status.HTTP_200_OK
        return data[0]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response


@app.delete("/categories/{id}")
async def categories_6(response: Response, id: int):
    app.db_connection.row_factory = aiosqlite.Row

    cursor = await app.db_connection.execute(
        """
        SELECT EXISTS(SELECT 1 FROM Categories WHERE CategoryID=:id) as if_exist
        """, {'id': id})
    data = await cursor.fetchall()
    if_exist = data[0]['if_exist']
    if if_exist == 1:
        # response.status_code = status.HTTP_200_OK
        cursor = app.db_connection.execute(
            """
            delete from Categories
            where CategoryID =:id
            """, {'id': id})
        data = await cursor.fetchall()
        return {"deleted": 1}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response


