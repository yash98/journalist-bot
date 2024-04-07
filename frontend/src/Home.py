import streamlit as st
from config_loader import app_config
from streamlit_oauth import OAuth2Component
import os

def main():
    st.title("Dynamic Survey")

    AUTHORIZE_URL = app_config["oauth"]["AUTHORIZE_URL"]
    TOKEN_URL = app_config["oauth"]["TOKEN_URL"]
    REFRESH_TOKEN_URL = app_config["oauth"]["REFRESH_TOKEN_URL"]
    REVOKE_TOKEN_URL = app_config["oauth"]["REVOKE_TOKEN_URL"]
    CLIENT_ID = os.getenv("GOOGLE_OATH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_OATH_CLIENT_SECRET")
    REDIRECT_URI = app_config["oauth"]["REDIRECT_URI"]
    SCOPE = app_config["oauth"]["SCOPE"]
    
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    # Check if token exists in session state
    if 'token' not in st.session_state:
        # If not, show authorize button
        result = oauth2.authorize_button("Login with Google", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            # If authorization successful, save token in session state
            st.session_state.token = result.get('token')
            st.rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state['token']
        st.json(token)
        if st.button("Refresh Token"):
            # If refresh token button is clicked, refresh the token
            token = oauth2.refresh_token(token)
            st.session_state.token = token
            st.rerun()

if __name__ == "__main__":
    main()
