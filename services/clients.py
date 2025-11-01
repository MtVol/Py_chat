from openai import OpenAI
from dotenv import load_dotenv
import os

# Carga las variables de entorno una sola vez al iniciar
load_dotenv()

# Crea una única instancia del cliente que será compartida
openai_client = OpenAI(
    api_key=os.getenv("OPENROUTE_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

def get_openai_client() -> OpenAI:
    """
    Función de dependencia que proporciona el cliente OpenAI compartido.
    """
    return openai_client