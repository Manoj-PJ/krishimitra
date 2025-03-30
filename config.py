import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ca2a08c620411b3c31a161eadecc60f7e5466612f165b203')
    SQLALCHEMY_DATABASE_URI = 'instance:///krishimitra.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False