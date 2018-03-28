import requests
import json

MAX_RETRIES = 3

class TRKD:
    def __init__(self, userId, appId, password):
        self.userId = userId
        self.appId = appId
        self.password = password
        self.headers = {"Content-Type": "application/json"}

    def login(self):
        url = "https://api.trkd.thomsonreuters.com/api/TokenManagement/TokenManagement.svc/REST/Anonymous/TokenManagement_1/CreateServiceToken_1"
        body = {
            "CreateServiceToken_Request_1": {
                "ApplicationID": self.appId,
                "Username": self.userId,
                "Password": self.password
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        if r.status_code == 200:
            self.token = r.json()['CreateServiceToken_Response_1']['Token']
            self.headers['X-Trkd-Auth-Token'] = self.token
            self.headers['X-Trkd-Auth-ApplicationID'] = self.appId
            return True
        else:
            return False

    def __get_data(self, url, data, tries=0):
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 500 and tries < MAX_RETRIES:  # TOKEN EXPIRED
            print("TOKEN EXPIRED")
            print(response)

            self.login()
            return self.__get_data(url, data, tries + 1)
        else:
            print("REQUEST ERROR")
            print(response)
            return None

    def get_quotes(self, ric):
        url = "http://api.trkd.thomsonreuters.com/api/Quotes/Quotes.svc/REST/Quotes_1/RetrieveItem_3"
        body = {
            "RetrieveItem_Request_3": {
                "ItemRequest": [{"RequestKey": [{"Name": ric, "NameType": "RIC"}], "Scope": "All"}],
                "TrimResponse": False,
                "IncludeChildItemQoS": False
            }
        }
        response = self.__get_data(url, json.dumps(body))
        if response is not None:
            return response.json()["RetrieveItem_Response_3"]

        return None

    def get_quotelist(self, rics, tries=0):
        url = "http://api.trkd.thomsonreuters.com/api/Quotes/Quotes.svc/REST/Quotes_1/RetrieveItem_3"
        body = {
            "RetrieveItem_Request_3": {
                "ItemRequest": [{"RequestKey": [{"Name": ric, "NameType": "RIC"} for ric in rics], "Scope": "All"}],
                "TrimResponse": False,
                "IncludeChildItemQoS": False
            }
        }
        response = self.__get_data(url, json.dumps(body))
        if response is not None:
            return response.json()["RetrieveItem_Response_3"]

        return None

    def get_news_headlines(self, filter, tries=0):
        url = "http://api.trkd.thomsonreuters.com/api/News/News.svc/REST/News_1/RetrieveHeadlineML_1"
        body = {"RetrieveHeadlineML_Request_1":
            {"HeadlineMLRequest":
                {
                    "Direction": "Newer",
                    "Filter": filter
                }
            }
        }
        response = self.__get_data(url, json.dumps(body))
        print(response)
        if response is not None:
            return response

        return None

    def online_reports_get_topics(self):
        url = "http://api.trkd.thomsonreuters.com/api/OnlineReports/OnlineReports.svc/REST/OnlineReports_1/GetTopics_2"
        body = {
            "GetTopics_Request_2": {}
        }
        response = self.__get_data(url, json.dumps(body))
        print(response)
        if response is not None:
            return response

        return None

    def online_reports_get_headlines(self, topic):
        url = "http://api.trkd.thomsonreuters.com/api/OnlineReports/OnlineReports.svc/REST/OnlineReports_1/GetHeadlines_2"
        body = {
            "GetHeadlines_Request_2": {
                "Topic": topic
            }
        }
        response = self.__get_data(url, json.dumps(body))
        print(response)
        if response is not None:
            return response

        return None

    def top_news_get_columns(self):
        url = "http://api.trkd.thomsonreuters.com/api/TopNews/TopNews.svc/REST/TopNews_1/GetTopNewsColumns_1"
        body = {
            "GetTopNewsColumns_Request_1": {}
        }
        response = self.__get_data(url, json.dumps(body))
        print(response)
        if response is not None:
            return response

        return None

    def top_news_get_top_news(self, columnId):
        url = "http://api.trkd.thomsonreuters.com/api/TopNews/TopNews.svc/REST/TopNews_1/RetrieveTopNewsByColumnID_1"
        body = {
            "RetrieveTopNewsByColumnID_Request_1": {
                "ColumnId": columnId
            }
        }
        response = self.__get_data(url, json.dumps(body))
        print(response)
        if response is not None:
            return response

        return None


