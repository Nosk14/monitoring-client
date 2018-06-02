import os
import RPi.GPIO as GPIO
from time import sleep
from dht22 import DHT22
from client import Client
from datetime import datetime


GPIO.setmode(GPIO.BCM)


class Monitor(object):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, pin, zone, api_endpoint, freq):
        super().__init__()
        self.__dht = DHT22(pin)
        self.frequency = freq
        self.client = Client(zone, api_endpoint)

    def run(self):
        while True:
            h, t, e = self.__dht.read_data()
            if not e:
                self.client.send_data(t, h, datetime.now())
                sleep(self.frequency)
            else:
                sleep(30)


if __name__ == '__main__':
    frequency = os.environ.get("FREQUENCY", 600)
    endpoint = os.environ.get("ENDPOINT", 'http://localhost:5000')
    pin = os.environ.get("PIN", 4)
    zone = os.environ.get("ZONE")
    if not zone:
        raise Exception("A zone must be specified")

    monitor = Monitor(int(pin), zone, endpoint, int(frequency))
    monitor.run()

