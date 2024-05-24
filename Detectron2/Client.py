import json
import requests

class Client:
    def __init__(self, id):
        self._id = id
        self.baseUrl = "http://192.168.1.182:5000"
        self._url = self.baseUrl + "/admin/people/amount"

    def PostPeopleCount(self, request):
        req = json.dumps(request)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(self._url, data=req, headers=headers)
        return response.text