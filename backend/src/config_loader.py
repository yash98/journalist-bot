import toml
import os

app_config = toml.load('config.toml')

GOOGLE_OATH_CLIENT_ID = os.getenv("GOOGLE_OATH_CLIENT_ID")
GOOGLE_OATH_CLIENT_SECRET = os.getenv("GOOGLE_OATH_CLIENT_SECRET")
