from fastapi.testclient import TestClient
from main import app
import pytest
from datetime import date, timedelta
client = TestClient(app)


# Test Get Root 1.1
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"



# Test Get Method 1.2
def test_method():
    method_endpoint = "/method"
    response = client.get(method_endpoint)
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

    response = client.delete(method_endpoint)
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

    response = client.put(method_endpoint)
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

    response = client.options(method_endpoint)
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}

    response = client.post(method_endpoint)
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}



# Test Get Password 1.3
def test_auth_right():
    password = '?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215'
    response = client.get(f"/auth{password}")
    assert response.status_code == 204


def test_auth_right_2():
    password = '?password=yshjlkdfgdfgh&password_hash=40c625f01a2537a4e0838f2f2f16afe287e4e193af57e2d48307705a2bcbcaf93aa892f0d7467f53e47b95f33d89344723800b4d674b01b99bd78af07e24d4ae'
    response = client.get(f"/auth{password}")
    assert response.status_code == 204


def test_auth_wrong():
    password = '?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091'
    response = client.get(f"/auth{password}")
    assert response.status_code == 401


def test_auth_wrong_v2():
    password = '?password=GeeksforGeeks&password_hash=0d8fb9370a5bf7b892be4865cdf8b658a82209624e33ed71cae353b0df254a75db63d1baa35ad99f26f1b399c31f3c666a7fc67ecef3bdcdb7d60e8ada90b722'
    response = client.get(f"/auth{password}")
    assert response.status_code == 204


def test_auth_wrong_v3():
    password = '?password=&password_hash='
    response = client.get(f"/auth{password}")
    assert response.status_code == 401


def test_auth_wrong_v4():
    password = '?password=&password_hash=cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
    response = client.get(f"/auth{password}")
    assert response.status_code == 401


def test_auth_wrong_v5():
    password = '?password=&password_hash='
    response = client.get(f"/auth{password}")
    assert response.status_code == 401


def number_of_letters(word):
    result = 0
    for character in word:
        if character.isalpha():
            result += 1
    return result


# Test Post Register 1.4
def test_register():
    response = client.post(f"/register",
                           json={"name": "Jan", "surname": "Nowak"})

    register_date = date.today()
    days_to_add = number_of_letters("Jan") + number_of_letters("Nowak")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 1,
                               "name": "Jan",
                               "surname": "Nowak",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test2_post():
    response = client.post(f"/register",
                           json={"name": "Kamil", "surname": "Nosal"})

    register_date = date.today()
    days_to_add = number_of_letters("Kamil") + number_of_letters("Nosal")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 2,
                               "name": "Kamil",
                               "surname": "Nosal",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test3_post():
    response = client.post(f"/register",
                           json={"name": "Krzysiek", "surname": "Koperek"})

    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 3,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test4_post():
    response = client.post(f"/register",
                           json={"name": "Krzysiek", "surname": "Koperek"})

    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 4,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test5_post():
    response = client.post(f"/register",
                           json={"name": "Krzysiek", "surname": "Koperek"})

    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 5,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test6_post():
    response = client.post(f"/register",
                           json={"name": "Krzysiek", "surname": "Koperek"})

    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 6,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201


def test7_post():
    response = client.post(f"/register",
                           json={"name": "Krzysiek", "surname": "Koperek"})

    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 7,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 201



# Test Get Patient 1.5
def test_patient_it():
    id_of_patient = 1
    response = client.get(f"/patient/{id_of_patient}")

    register_date = date.today()
    days_to_add = number_of_letters("Jan") + number_of_letters("Nowak")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": id_of_patient,
                               "name": "Jan",
                               "surname": "Nowak",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 200


def test_patient_it_2():
    id_of_patient = 2
    response = client.get(f"/patient/{id_of_patient}")

    register_date = date.today()
    days_to_add = number_of_letters("Kamil") + number_of_letters("Nosal")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 2,
                               "name": "Kamil",
                               "surname": "Nosal",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 200


def test_patient_it_7():
    id_of_patient = 7
    response = client.get(f"/patient/{id_of_patient}")
    register_date = date.today()
    days_to_add = number_of_letters("Krzysiek") + number_of_letters("Koperek")
    vaccination_date = register_date + timedelta(days_to_add)

    assert response.json() == {"id": 7,
                               "name": "Krzysiek",
                               "surname": "Koperek",
                               "register_date": str(register_date),
                               "vaccination_date": str(vaccination_date)}
    assert response.status_code == 200


def test_patient_it_wrong():
    id_of_patient = 8
    response = client.get(f"/patient/{id_of_patient}")

    assert response.status_code == 404


def test_patient_it_wrong_2():
    id_of_patient = 10
    response = client.get(f"/patient/{id_of_patient}")

    assert response.status_code == 404


def test_patient_it_wrong_3():
    id_of_patient = 0
    response = client.get(f"/patient/{id_of_patient}")

    assert response.status_code == 400


def test_patient_it_wrong_4():
    id_of_patient = -1
    response = client.get(f"/patient/{id_of_patient}")

    assert response.status_code == 400


"""nie dziala bo data jest niepoprawna"""
# def test_hello():
#     # todays_date = date.today()
#     response = client.get(f"/hello")
#     assert response.text == f"""
#         <html>
#             <head>
#                 <title>have no idea whether it works</title>
#             </head>
#             <body>
#                 <h1>Hello! Today date is {date.today()}</h1>
#             </body>
#         </html>
#         """
#     assert response.status_code == 200


def test_products():
    id_of_patient = 1
    response = client.get(f"/products/{id}")
    for i in range(1,70):
        response = client.get(f"/products/{i}")
        assert response.status_code == 200
