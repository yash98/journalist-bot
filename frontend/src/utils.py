from config_loader import app_config
from streamlit_oauth import OAuth2Component
import os
import streamlit as st
from constants import *
import math
import time

AUTHORIZE_URL = app_config["oauth"]["AUTHORIZE_URL"]
TOKEN_URL = app_config["oauth"]["TOKEN_URL"]
REFRESH_TOKEN_URL = app_config["oauth"]["REFRESH_TOKEN_URL"]
REVOKE_TOKEN_URL = app_config["oauth"]["REVOKE_TOKEN_URL"]
GOOGLE_OATH_CLIENT_ID = os.getenv("GOOGLE_OATH_CLIENT_ID")
GOOGLE_OATH_CLIENT_SECRET = os.getenv("GOOGLE_OATH_CLIENT_SECRET")
REDIRECT_URI = app_config["oauth"]["REDIRECT_URI"]
SCOPE = app_config["oauth"]["SCOPE"]
OATH2 = OAuth2Component(GOOGLE_OATH_CLIENT_ID, GOOGLE_OATH_CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

def refresh_token_if_needed():
    if st.session_state[SESSION_TOKEN_KEY]["expires_at"] <= math.floor(time.time()):
        token = OATH2.refresh_token(st.session_state[SESSION_TOKEN_KEY])
        st.session_state[SESSION_TOKEN_KEY] = token