import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# OLX Search Configuration
OLX_BASE_URL = "https://www.olx.uz"
OLX_API_URL = "https://www.olx.uz/api/v1/offers/"
OLX_REQUEST_TIMEOUT = 15
OLX_SEARCH_LIMIT = 20

# User-Agent & Impersonation for CloudFront / WAF bypass
CHROME_IMPERSONATE = "chrome120"
DEFAULT_PHOTO_PLACEHOLDER = "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800"
