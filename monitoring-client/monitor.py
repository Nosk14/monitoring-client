import os
import RPi.GPIO as GPIO
import logging as log
from time import sleep
from dht22 import DHT22
from client import Client
from datetime import datetime
from pytz import timezone

GPIO.setmode(GPIO.BCM)


class Monitor(object):
    TZ = timezone('Europe/Madrid')
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, pin, zone, api_endpoint, freq):
        super().__init__()
        self.__dht = DHT22(pin)
        self.frequency = freq
        self.zone = zone
        self.client = Client(zone, api_endpoint)

    def run(self):
        while True:
            h, t, e = self.__dht.read_data()
            if not e:
                self.client.send_data(t, h, datetime.now().replace(tzinfo=self.TZ))
                log.info("Data sent correctly [{}, {}, {}]".format(self.zone, t, h))
                sleep(self.frequency)
            else:
                log.warning("Error reading data [{}, {}, {}]".format(self.zone, t, h))
                sleep(30)


if __name__ == '__main__':
    frequency = os.environ.get("FREQUENCY", 600)
    endpoint = os.environ.get("ENDPOINT", 'http://localhost:5000')
    pin = os.environ.get("PIN", 4)
    zone = os.environ.get("ZONE")
    if not zone:
        raise Exception("A zone must be specified")

    log_level = os.environ.get("LOG_LEVEL", 20)
    log.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=log_level)

    monitor = Monitor(int(pin), zone, endpoint, int(frequency))
    monitor.run()

