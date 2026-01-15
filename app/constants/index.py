import os

from dotenv import load_dotenv

load_dotenv()

ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY", "---MISSING---")
ZERODHA_API_SECRET = os.getenv("ZERODHA_API_SECRET", "---MISSING---")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN", "---MISSING---")

# FRONTEND_URLS should be a comma-separated list of URLs
FRONTEND_URLS = os.getenv("FRONTEND_URLS", "*")
ALLOWED_ORIGINS = [url.strip() for url in FRONTEND_URLS.split(",")] if FRONTEND_URLS != "*" else ["*"]
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
