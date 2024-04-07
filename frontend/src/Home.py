import streamlit as st
from constants import *
from utils import *
import time
import math

def main():
    if SESSION_USER_NAME_KEY in st.session_state and SESSION_TOKEN_KEY in st.session_state:
        st.title(f"Welcome {st.session_state[SESSION_USER_NAME_KEY]}")
    else:
        st.title("Dynamic Survey")

    # Check if token exists in session state
    if SESSION_TOKEN_KEY not in st.session_state:
        # If not, show authorize button
        result = OATH2.authorize_button("Login with Google", REDIRECT_URI, SCOPE)
        if result and SESSION_TOKEN_KEY in result:
            # If authorization successful, save token in session state
            st.session_state[SESSION_TOKEN_KEY] = result.get(SESSION_TOKEN_KEY)
            st.rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state[SESSION_TOKEN_KEY]
        # "expires_at":1712421356 < time in milliseconds
        if token["expires_at"] <= math.floor(time.time()):
            # If refresh token button is clicked, refresh the token
            token = OATH2.refresh_token(token)
            st.session_state[SESSION_TOKEN_KEY] = token
        if st.button("Logout"):
            OATH2.revoke_token(st.session_state[SESSION_TOKEN_KEY][SESSION_ID_TOKEN_KEY], SESSION_ID_TOKEN_KEY)
            OATH2.revoke_token(st.session_state[SESSION_TOKEN_KEY][SESSION_ACCESS_TOKEN_KEY], SESSION_ACCESS_TOKEN_KEY)
            del st.session_state[SESSION_TOKEN_KEY]
            del st.session_state[SESSION_USER_NAME_KEY]
            st.rerun()

if __name__ == "__main__":
    main()
