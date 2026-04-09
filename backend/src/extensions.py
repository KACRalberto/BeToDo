from flask_jwt_extended import JWTManager, create_access_token
from flask_mysqldb import MySQL



conexion = MySQL()
jwt = JWTManager()


def crear_token(data):
    return create_access_token(identity=data)