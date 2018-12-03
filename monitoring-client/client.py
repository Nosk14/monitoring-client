import requests
import logging as log


class Client:
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, zone, endpoint):
        self.endpoint = endpoint
        self.zone = zone

    def send_data(self, data):
        log.debug("Data sent: [{}]".format(str(data)))
        requests.put(self.endpoint, json=data, headers=self.HEADERS)
