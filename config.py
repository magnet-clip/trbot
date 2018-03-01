from configparser import ConfigParser
import json
from typing import List, Tuple, Optional


class Ric:
    def __init__(self, ric, name):
        self.ric = ric
        self.name = ric if ric != "" else name


class Publish:
    def __init__(self, data):
        self.schedule = data['schedule']
        self.rics = []
        for ric in data['rics']:
            self.rics.append(Ric(ric, data['rics'][ric]))

    def get_rics(self) -> List[Ric]:
        return self.rics


class Channel:
    def __init__(self, data):
        self.name = data['name']
        self.address = data['address']
        self.publications = []

        if isinstance(data['publish'], list):
            for publish in data['publish']:
                self.publications.append(Publish(publish))
        else:
            self.publications.append(Publish(data['publish']))

    def get_publications(self) -> List[Publish]:
        return self.publications


class Config:
    def __init__(self, filename, fname):
        self.config = ConfigParser()
        self.config.read_file(open(filename))
        self.channels = [Channel(channel) for channel in json.load(open(fname, encoding="utf8"))]

    def telegram_api_key(self):
        return self.config['Telegram']['api_key']

    def get_admins(self):
        admins = self.config['Bot']['admins']
        print(admins)
        if len(admins) > 0:
            return list(map(int, map(str.strip, admins.split(","))))

        return []

    def get_channel_names(self):
        return list(map(lambda x: x.name, self.channels))

    def get_trkd_credentials(self):
        return self.config['Trkd']['username'], self.config['Trkd']['app_id'], self.config['Trkd']['password']

    def get_channel_id(self, name):
        for item in self.channels:
            if item.name == name:
                return item.address

        return None

    def get_db_host(self) -> str:
        return self.config['Db']['url']

    def get_db_user(self) -> str:
        return self.config['Db']['login']

    def get_db_password(self) -> str:
        return self.config['Db']['password']

    def get_db_name(self) -> str:
        return self.config['Db']['db']

    def get_version(self) -> str:
        return self.config['Version']['version']

    def get_facebook(self) -> Tuple[str, str]:
        return self.config['Facebook']['app_id'], self.config['Facebook']['app_secret']

    def get_channels(self) -> List[Channel]:
        return self.channels

    def get_channel_by_name(self, channel_name) -> Optional[Channel]:
        for channel_info in self.channels:
            if channel_info.name == channel_name:
                return channel_info

        return None

    def get_channel_by_id(self, channel_id) -> Optional[Channel]:
        for channel_info in self.channels:
            if channel_info.address == channel_id:
                return channel_info

        return None
