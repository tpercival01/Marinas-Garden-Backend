from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY must be set in environment variables")

groq_client = OpenAI(api_key=GROQ_API_KEY,  base_url="https://api.groq.com/openai/v1")

