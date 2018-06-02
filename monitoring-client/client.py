import requests
import logging as log


class Client(object):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, zone, endpoint):
        self.endpoint = endpoint
        self.zone = zone
        self.dat_endpoint = "{}/data".format(self.endpoint)

    def send_data(self, temperature, humidity, time):
        data = {
            "zone": self.zone,
            "data": [
                {
                    "time": time.strftime(self.DATE_FORMAT),
                    "temperature": temperature,
                    "humidity": humidity
                }
            ]
        }
        log.debug("Data sent: [{}]".format(str(data)))
        requests.put(self.dat_endpoint, json=data, headers=self.HEADERS)
