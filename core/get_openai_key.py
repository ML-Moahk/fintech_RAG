#The reason why i have this file is because FastApi is having difficulties loading my file with 
#openAI so I will be creating an openAI function with dotevn to load the api key directly from 
#the function 

from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError( "OpenAI key not found in environmrnt" )
    return OpenAI(api_key=api_key)

