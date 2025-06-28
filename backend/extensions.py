from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis

mysql = MySQL()
jwt = JWTManager()
cors = CORS()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

