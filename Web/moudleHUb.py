#!/usr/bin/python
# encoding:utf-8

import RPi.GPIO as GPIO
import time
import smbus
import math

DHTPIN = 4

GPIO.setmode(GPIO.BCM)

# 引脚输出模式初始化
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

bus = smbus.SMBus(1)
address = 0x0d


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low

    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)


def readGIS():
    """
    很好，这就读坐标函数

    """
    write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000)  # Continuous sampling

    scale = 0.92
    x_offset = -39
    y_offset = -100

    x_out = (read_word_2c(3) - x_offset) * scale
    y_out = (read_word_2c(7) - y_offset) * scale

    bearing = math.atan2(x_out, y_out)
    if bearing < 0:
        bearing += 2 * math.pi
    print("Bearing:", math.degrees(bearing))
    print(x_out)
    print(y_out)
    return "Bearing:" + str(math.degrees(bearing)) + x_out + " " + y_out


def read_distance():
    """
    很好，这就是超声波测距函数

    """
    GPIO.output(23, True)
    time.sleep(0.005)
    GPIO.output(23, False)

    while GPIO.input(24) == 0:
        signaloff = time.time()

    while GPIO.input(24) == 1:
        signalon = time.time()

    timepassed = signalon - signaloff
    distance = timepassed * 17000
    return 'Distance: %f cm' % read_distance()


# 读取dht11传感器数据
def read_dht11_dat():
    MAX_UNCHANGE_COUNT = 100

    STATE_INIT_PULL_DOWN = 1
    STATE_INIT_PULL_UP = 2
    STATE_DATA_FIRST_PULL_DOWN = 3
    STATE_DATA_PULL_UP = 4
    STATE_DATA_PULL_DOWN = 5
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(DHTPIN)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        print("Data not good, skip")
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    # print "bits: %s, length: %d" % (bits, len(bits))
    for i in range(0, len(bits)):
        byte = byte << 1
        if bits[i]:
            byte = byte | 1
        else:
            byte = byte | 0
        if (i + 1) % 8 == 0:
            the_bytes.append(byte)
            byte = 0
            # print the_bytes
    checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        print("Data not good, skip")
        return False

    return the_bytes[0], the_bytes[2]


def TemperatureHumidity():
    global temperature, humidity
    try:

        result = read_dht11_dat()
        if result:
            humidity, celsius = result
            temperature = celsius
            print("Humidity: %s%%,  Temperature: %s C`" % (humidity, temperature))
            temperature = str(temperature)
            humidity = str(humidity)
    except KeyboardInterrupt:
        GPIO.cleanup()
    return 'temperature:' + str(temperature) + ' humidity:' + str(humidity)


class Peins:
    def __init__(self):
        self._DHTPIN = 4

        GPIO.setup(DHTPIN, GPIO.OUT)

    def _read_dht11_dat(self):
        MAX_UNCHANGE_COUNT = 100

        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        GPIO.setup(DHTPIN, GPIO.OUT)
        GPIO.output(self._DHTPIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self._DHTPIN, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(self._DHTPIN, GPIO.IN, GPIO.PUD_UP)

        unchanged_count = 0
        last = -1
        data = []
        while True:
            current = GPIO.input(self._DHTPIN)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > MAX_UNCHANGE_COUNT:
                    break

        state = STATE_INIT_PULL_DOWN

        lengths = []
        current_length = 0

        for current in data:
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_INIT_PULL_UP
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    state = STATE_DATA_FIRST_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_DATA_PULL_UP
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                else:
                    continue
        if len(lengths) != 40:
            print("Data not good, skip")
            return False

        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0

        for length in lengths:
            bit = 0
            if length > halfway:
                bit = 1
            bits.append(bit)
        # print "bits: %s, length: %d" % (bits, len(bits))
        for i in range(0, len(bits)):
            byte = byte << 1
            if bits[i]:
                byte = byte | 1
            else:
                byte = byte | 0
            if (i + 1) % 8 == 0:
                the_bytes.append(byte)
                byte = 0
                # print the_bytes
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            print("Data not good, skip")
            return False

        return the_bytes[0], the_bytes[2]

    def _TemperatureHumidity(self):
        global temperature, humidity
        try:

            result = self._read_dht11_dat()
            if result:
                humidity, celsius = result
                temperature = celsius
                print("Humidity: %s%%,  Temperature: %s C`" % (humidity, temperature))
                temperature = str(temperature)
                humidity = str(humidity)
        except KeyboardInterrupt:
            GPIO.cleanup()
        return 'temperature:' + str(temperature) + ' humidity:' + str(humidity)

