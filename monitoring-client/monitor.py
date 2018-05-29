import os
import RPi.GPIO as GPIO
from time import sleep
from dht22 import DHT22
from client import Client
from datetime import datetime


GPIO.setmode(GPIO.BCM)


class Monitor(object):
    ZONE = "test"
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, pin, api_endpoint, freq):
        super().__init__()
        self.__dht = DHT22(pin)
        self.frequency = freq
        self.client = Client(self.ZONE, api_endpoint)

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

    monitor = Monitor(int(pin), endpoint, int(frequency))
    monitor.run()

