import streamlit as st

def main():
    st.title("Dynamic Survey")

    if st.button("Sign in with Google"):
        # Redirect the user to the Google Sign-In page
        auth_url = "https://accounts.google.com/o/oauth2/auth"
        client_id = "1040282229654-ir49kts7gk23gin6s07ksee96cb8crga.apps.googleusercontent.com"  # Replace with your actual client ID
        redirect_uri = "http://localhost:8501/"  # Replace with your redirect URI
        # scope = "openid"  # Replace with the desired scopes
        # state = "state123"  # Replace with a unique state value
        # auth_endpoint = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
        auth_endpoint = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
        st.markdown(f'<a href="{auth_endpoint}">Click here to sign in with Google</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
