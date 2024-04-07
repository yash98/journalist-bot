from config_loader import app_config
from streamlit_oauth import OAuth2Component
import os

AUTHORIZE_URL = app_config["oauth"]["AUTHORIZE_URL"]
TOKEN_URL = app_config["oauth"]["TOKEN_URL"]
REFRESH_TOKEN_URL = app_config["oauth"]["REFRESH_TOKEN_URL"]
REVOKE_TOKEN_URL = app_config["oauth"]["REVOKE_TOKEN_URL"]
CLIENT_ID = os.getenv("GOOGLE_OATH_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_OATH_CLIENT_SECRET")
REDIRECT_URI = app_config["oauth"]["REDIRECT_URI"]
SCOPE = app_config["oauth"]["SCOPE"]
OATH2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)