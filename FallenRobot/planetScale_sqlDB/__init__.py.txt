import pymysql
from FallenRobot import con


def start() -> pymysql.connections.Connection:
    connection = con
    return connection


SESSION = start()
