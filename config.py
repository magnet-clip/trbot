from configparser import ConfigParser


class Config:
    channels = [{
            "address": "@tr_commodities_metals",
            "name": "Metals"
        }, {
            "address": "@tr_commodities_agriculture",
            "name": "Agriculture"
        }, {
            "address": "@tr_commodities_energy",
            "name": "Energy"
        }
    ]

    def __init__(self, filename):
        self.config = ConfigParser()
        self.config.read_file(open(filename))

    def telegram_api_key(self):
        return self.config['Telegram']['api_key']

    def get_admins(self):
        admins = self.config['Bot']['admins']
        print(admins)
        if len(admins) > 0:
            return list(map(int, map(str.strip, admins.split(","))))

        return []

    def get_channel_names(self):
        return list(map(lambda x: x["name"], self.channels))

    def get_channel_id(self, name):
        for item in self.channels:
            if item['name'] == name:
                return item['address']

        return None

    def get_db_host(self):
        return self.config['Db']['url']

    def get_db_user(self):
        return self.config['Db']['login']

    def get_db_password(self):
        return self.config['Db']['password']

    def get_db_name(self):
        return self.config['Db']['db']
