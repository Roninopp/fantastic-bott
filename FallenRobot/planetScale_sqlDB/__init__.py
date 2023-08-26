import pymysql
from Powers import con


def start() -> pymysql.connections.Connection:
    connection = con
    return connection


SESSION = start()
