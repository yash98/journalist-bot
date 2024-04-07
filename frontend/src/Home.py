import streamlit as st
from constants import *
from utils import *
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

# import streamlit_debug
# streamlit_debug.set(flag=True, wait_for_client=True, host='localhost', port=8765)

def main():
    if SESSION_USER_NAME_KEY in st.session_state and SESSION_TOKEN_KEY in st.session_state:
        st.title(f"Welcome {st.session_state[SESSION_USER_NAME_KEY]}")
    else:
        st.title("Dynamic Survey")

    if SESSION_TOKEN_KEY not in st.session_state:
        result = OATH2.authorize_button("Login with Google", REDIRECT_URI, SCOPE)
        if result and SESSION_TOKEN_KEY in result:
            st.session_state[SESSION_OATH_KEY] = result
            st.session_state[SESSION_TOKEN_KEY] = result.get(SESSION_TOKEN_KEY)
            id_info = None
            try:
                id_info = id_token.verify_oauth2_token(result[SESSION_ID_TOKEN_KEY], requests.Request(), GOOGLE_OATH_CLIENT_ID)
                st.session_state[SESSION_USER_INFO_KEY] = id_info
                st.session_state[SESSION_USER_NAME_KEY] = id_info["name"]
            except Exception as e:
                st.error(f"Auth error: {e}")
                logging.exception("Failed with authenticating id token: " + str(e))
            # print("id_info: ", id_info)
            email = id_info["email"]
            st.rerun()
    else:
        refresh_token_if_needed()

        if st.button("Logout"):
            OATH2.revoke_token(st.session_state[SESSION_OATH_KEY][SESSION_ID_TOKEN_KEY], SESSION_ID_TOKEN_KEY)
            OATH2.revoke_token(st.session_state[SESSION_OATH_KEY][SESSION_ACCESS_TOKEN_KEY], SESSION_ACCESS_TOKEN_KEY)
            del st.session_state[SESSION_TOKEN_KEY]
            del st.session_state[SESSION_USER_NAME_KEY]
            st.rerun()

if __name__ == "__main__":
    main()
