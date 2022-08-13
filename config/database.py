
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.Sprint4
colection_dados = db.dados
colection_users = db.users
