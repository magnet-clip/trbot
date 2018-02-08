import requests, json
from datetime import datetime


class Dss:
    headers = {'Content-Type': 'application/json; odata.metadata=minimal'}

    def __init__(self, login, password):
        self.password = password
        self.login = login
        self.token = ""

    def authenticate(self):
        url_get_token = 'https://hosted.datascopeapi.reuters.com/RestApi/v1/Authentication/RequestToken'
        login_data = json.dumps({'Credentials': {'Password': self.password, 'Username': self.login}})
        resp = requests.post(url_get_token, login_data, headers=self.headers)
        if resp.status_code != 200:
            print('ERROR, ' + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ', Get Token failed with ' + str(resp.status_code))
            return False
        else:
            j = resp.json()
            self.token = j["value"]
            return True

    def get_ric_history(self):
        pass
