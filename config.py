from configparser import ConfigParser


class Config:
    METALS = "metals"
    AGRO = "agriculture"
    ENERGY = "energy"

    channels = {
        METALS: "@tr_commodities_metals",
        AGRO: "@tr_commodities_agriculture",
        ENERGY: "@tr_commodities_energy"
    }

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
