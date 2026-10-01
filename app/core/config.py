"""Application configuration.

Later we will load environment variables and AI provider settings here.
"""
import os

from dotenv import load_dotenv


load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")