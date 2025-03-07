import os
from dotenv import load_dotenv
import requests

# Load .env from parent directory
# Dynamically find the parent directory and the .env file path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(parent_dir, ".env")
load_dotenv(env_path)

client_id = os.getenv("OA2_CLIENT_ID")
client_secret = os.getenv("OA2_CLIENT_SECRET")
redirect_uri = os.getenv("OA2_REDIRECT_URI")
token_url = os.getenv("OA2_TOKEN_URL")

# Headers for the POST request
headers_post = {
    "Content-Type": "application/x-www-form-urlencoded"
}
# Headers for the GET request
headers_get = lambda access_token : {
    "Authorization": f"Bearer {access_token}"
}
user_url = "https://discord.com/api/users/@me"

# URL pour échanger le code contre un token d'accès
token_url = "https://discord.com/api/oauth2/token"

class OAuth2Exception(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

oa2_error = OAuth2Exception("Code incorrect")

class OA2:
    def __init__(self):
        if not (client_id and client_secret and redirect_uri and token_url):
            raise Exception("Missing OA2 environment variables")
    def __get_token_from_code (self, code):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        # Échange du code contre un token d'accès
        response = requests.post(token_url, data=data, headers=headers_post)
        if response.status_code != 200:
            raise oa2_error

        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise oa2_error

        return access_token

    def __get_user_data_from_token (self, token):
        # Utilisation du token pour récupérer les informations utilisateur
        user_response = requests.get(user_url, headers=headers_get(token))
        if user_response.status_code != 200:
            raise oa2_error
        user_response = user_response.json()
        return user_response


    def get_user_data_from_code (self, code) -> dict :
        token: str = self.__get_token_from_code(code)

        user_data = self.__get_user_data_from_token(token)
        user_data["oa2_token"] = token
        return user_data