import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.models.groq import GroqTools

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API key desde las variables de entorno
groq_api_key = os.getenv('GROQ_API_KEY')

if not groq_api_key:
    raise ValueError("GROQ_API_KEY no está configurada en el archivo .env")

agent = Agent(
    instructions=[
        "You are a helpful assistant that can transcribe audio, translate text and generate speech."
    ],
    tools=[GroqTools()],
    )
