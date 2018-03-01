import requests
import json

from config import Config


class FacebookManager:
    def __init__(self, config: Config):
        app_id, app_secret = config.get_facebook()

        payload = {
            'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret
        }

        file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        response = json.loads(file.text)
        self.token = response['access_token']


if __name__ == "__main__":
    config = Config("../config.ini", "../channels.json")
    facebook = FacebookManager(config)
    print(facebook.token)
