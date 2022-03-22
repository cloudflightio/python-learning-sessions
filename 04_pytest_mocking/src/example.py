from time import sleep

from src.db import db_write

MY_CONSTANT = 10

def foo():
    x = db_write()  # x = MagicMock()
    return x

def check_status():
    result = long_api_call()
    return result["status"]


def long_api_call():
    sleep(2000)
    return {'status': 200}


def multiply_with_constant(nr: int):
    return nr * MY_CONSTANT

print(multiply_with_constant(3))
