from app.serializers.auth import BaseAuthSerializer, AuthToken
from app.models.auth import Auth

auth = BaseAuthSerializer(username="Mr Robot")

auth_json = {"username": "Mr Robot"}

token = AuthToken(access_token="verysecrettoken", token_type="bearer")

token_json = {
    "access_token": "verysecrettoken",
    "token_type": "bearer",
}

auth_model = Auth(username="Mr Robot", password="verysecretpassword")
