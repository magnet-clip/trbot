import requests
import json


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

    def getQuotes(self, ric):
        url = "http://api.trkd.thomsonreuters.com/api/Quotes/Quotes.svc/REST/Quotes_1/RetrieveItem_3"
        body = {
            "RetrieveItem_Request_3": {
                "ItemRequest": [{"RequestKey": [{"Name": ric, "NameType": "RIC"}], "Scope": "All"}],
                "TrimResponse": False,
                "IncludeChildItemQoS": False
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        if r.status_code == 200:
            return r.json()["RetrieveItem_Response_3"]
        else:
            return None

    def getQuotesList(self, rics):
        url = "http://api.trkd.thomsonreuters.com/api/Quotes/Quotes.svc/REST/Quotes_1/RetrieveItem_3"
        body = {
            "RetrieveItem_Request_3": {
                "ItemRequest": [{"RequestKey": [{"Name": ric, "NameType": "RIC"} for ric in rics], "Scope": "All"}],
                "TrimResponse": False,
                "IncludeChildItemQoS": False
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        if r.status_code == 200:
            return r.json()["RetrieveItem_Response_3"]
        else:
            return None

    def getNewsHeadlines(self, filter):
        url = "http://api.trkd.thomsonreuters.com/api/News/News.svc/REST/News_1/RetrieveHeadlineML_1"
        body = {"RetrieveHeadlineML_Request_1":
            {"HeadlineMLRequest":
                {
                    "Direction": "Newer",
                    "Filter": filter
                }
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        print(r)
        return r

    def onlineReportsGetTopics(self):
        url = "http://api.trkd.thomsonreuters.com/api/OnlineReports/OnlineReports.svc/REST/OnlineReports_1/GetTopics_2"
        body = {
            "GetTopics_Request_2": {}
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        print(r)
        return r

    def onlineReportsGetHeadlines(self, topic):
        url = "http://api.trkd.thomsonreuters.com/api/OnlineReports/OnlineReports.svc/REST/OnlineReports_1/GetHeadlines_2"
        body = {
            "GetHeadlines_Request_2": {
                "Topic": topic
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        print(r)
        return r

    def topNewsGetColumns(self):
        url = "http://api.trkd.thomsonreuters.com/api/TopNews/TopNews.svc/REST/TopNews_1/GetTopNewsColumns_1"
        body = {
            "GetTopNewsColumns_Request_1": {}
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        print(r)
        return r

    def topNewsGetTopNews(self, columnId):
        url = "http://api.trkd.thomsonreuters.com/api/TopNews/TopNews.svc/REST/TopNews_1/RetrieveTopNewsByColumnID_1"
        body = {
            "RetrieveTopNewsByColumnID_Request_1": {
                "ColumnId": columnId
            }
        }
        r = requests.post(url, data=json.dumps(body), headers=self.headers)
        print(r)
        return r


