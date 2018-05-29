import RPi.GPIO as GPIO
from time import sleep
from .dht22 import DHT22
from .client import Client


GPIO.setmode(GPIO.BCM)


class Monitor(object):
    ZONE = "test"
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, pin, api_endpoint, freq=600):
        super().__init__()
        self.__dht = DHT22(pin)
        self.frequency = freq
        self.client = Client(self.ZONE, api_endpoint)

    def run(self):
        while True:
            h, t, e = self.__dht.read_data()
            if not e:
                self.client.send_data(t, h)
                sleep(self.frequency)
            else:
                sleep(30)


if __name__ == '__main__':
    monitor = Monitor()

