import RPi.GPIO as GPIO
from time import sleep


COUNT_TIMEOUT = 50


class DHT22(object):

    def __init__(self, pin):
        self.pin = pin

    def read_data(self):
        signal = self.__read_signal()
        byte_list = self.__signal_to_bytes(signal)

        error = self.__checksum(byte_list)
        humidity = self.__calc_humidity(byte_list[0:2])
        temperature = self.__calc_temperature(byte_list[2:4])

        return humidity, temperature, error

    def __calc_humidity(self, bytes):
        return (bytes[0] * 256 + bytes[1])/float(10)

    def __calc_temperature(self, byte_list):
        msbyte = byte_list[0]
        sign = 1
        if 1 << 8 & msbyte:
            sign = -1
            msbyte &= 127

        return sign * (msbyte * 256 + byte_list[1])/float(10)

    def __checksum(self, byte_list):
        suma = sum(byte_list[:-1])
        mask = (suma << 8) - 1
        return (suma & mask) != byte_list[-1]

    def __read_signal(self):
        signals = [0 for _ in range(40)]

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(self.pin, GPIO.LOW)
        sleep(0.02)

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.__wait_while(GPIO.HIGH)
        self.__wait_while(GPIO.LOW)
        self.__wait_while(GPIO.HIGH)

        for bit in range(40):
            self.__wait_while(GPIO.LOW)
            while GPIO.input(self.pin):
                signals[bit] += 1
                if signals[bit] > COUNT_TIMEOUT:
                    raise TimeoutError("Signal timeout")

        return signals

    def __signal_to_bytes(self, signal):
        treshold = min(signal) * 1.8
        bits = [0 if x < treshold else 1 for x in signal]
        byte_list = []
        for i in range(5):
            bin_number = int(''.join(str(x) for x in bits[i*8:(i+1)*8]), base=2)
            byte_list.append(bin_number)
        return byte_list

    def __wait_while(self, value):
        count = 0
        while GPIO.input(self.pin) == value:
            count += 1
            if count > COUNT_TIMEOUT:
                raise TimeoutError("Signal timeout")

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def __str__(self):
        return '#'.join(str(x) for x in ['DHT22', self.pin])


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    d = DHT22(4)
    try:
        print(d.read_data())
    finally:
        d.cleanup()
