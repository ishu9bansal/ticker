import os

from dotenv import load_dotenv

load_dotenv()

ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY", "---MISSING---")
ZERODHA_API_SECRET = os.getenv("ZERODHA_API_SECRET", "---MISSING---")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN", "---MISSING---")
