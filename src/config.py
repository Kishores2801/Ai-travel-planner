# Loading the packages
import os
from dotenv import load_dotenv # dotenv is used to env




# Loading environmental variables from .env file
load_dotenv()


class Config:
    # loading config values
    ENV = os.getenv('ENV', 'development')
    DEBUG = ENV == 'development'

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash-lite')


    # Caching Configuration
    CACHE_TYPE = os.getenv('CACHE_BACKEND', 'memory')




config = Config()
   