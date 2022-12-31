import pymysql
from pymysql import cursors
from data import *

try:
    connection = pymysql.connect(
        host=HOST_DB,
        port=3306,
        user=USER_DB,
        password=PASSWORD_DB,
        database=NAME_DB,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected...")
    print("#" * 20)
except Exception as ex:
    print("Connection refused...")
    print(ex)