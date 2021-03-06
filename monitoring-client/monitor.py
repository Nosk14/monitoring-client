import os
import RPi.GPIO as GPIO
import logging as log
from time import sleep
from dht22 import DHT22
from client import Client
from datetime import datetime
from pytz import timezone
from requests.exceptions import RequestException

GPIO.setmode(GPIO.BCM)


class Monitor:
    TZ = timezone('Europe/Madrid')
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, pin, zone, api_endpoint, freq):
        self.__dht = DHT22(pin)
        self.frequency = freq
        self.zone = zone
        self.client = Client(zone, api_endpoint)

    def run(self):
        pending_data = []
        while True:
            h, t, e = self.__dht.read_data()
            if not e:
                pending_data.append(self.build_data(t, h, datetime.now(self.TZ)))
                try:
                    self.client.send_data(pending_data)
                    log.info("Data sent correctly [{}, {}, {}]".format(self.zone, t, h))
                    pending_data = []
                except RequestException as ex:
                    log.error("Error sending data: [{}]".format(ex))
                sleep(self.frequency)
            else:
                log.warning("Error reading data [{}, {}, {}]".format(self.zone, t, h))
                sleep(30)

    def build_data(self, temperature, humidity, time):
        return {
                    "time": time.strftime(self.DATE_FORMAT),
                    "temperature": temperature,
                    "humidity": humidity
                }

    def build_request(self, data):
        return {
            "zone": self.zone,
            "data": data
        }

if __name__ == '__main__':
    frequency = os.environ.get("FREQUENCY", 600)
    endpoint = os.environ.get("ENDPOINT", 'http://localhost:5000/data')
    pin = os.environ.get("PIN", 4)
    zone = os.environ.get("ZONE")
    if not zone:
        raise Exception("A zone must be specified")

    log_level = os.environ.get("LOG_LEVEL", 20)
    log.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=int(log_level))

    monitor = Monitor(int(pin), zone, endpoint, int(frequency))
    monitor.run()

