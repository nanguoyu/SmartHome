# encoding:utf-8

import RPi.GPIO as GPIO
import time

DHTPIN = 4
LightLED = 20
PersonAlarmLED = 19
SENSOR = 26
temperature, humidity = 26, 53
GPIO.setmode(GPIO.BCM)

# 引脚输出模式初始化
GPIO.setup(LightLED, GPIO.OUT)
GPIO.setup(PersonAlarmLED, GPIO.OUT)
GPIO.setup(DHTPIN, GPIO.OUT)


# 关灯
def turnOffLight():
    try:
        GPIO.output(LightLED, 0)
        print("turn off a light")
    except KeyboardInterrupt:
        GPIO.cleanup()


# 开灯
def turnOnLight():
    try:
        GPIO.output(LightLED, 1)
        print("turn On a light")
    except KeyboardInterrupt:
        GPIO.cleanup()


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


def AlarmMoudle():
    flag = False
    times = 0
    try:
        while times <= 10:
            # 检测人体红外是否输出低电平。若是输出低电平则表示声音被检测到，点亮关闭led
            if GPIO.input(SENSOR) == 1:
                flag = not flag
                print("有人来了")
                GPIO.output(PersonAlarmLED, flag)
            times = times + 1
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()


class Peins:
    def __init__(self):
        self._DHTPIN = 4
        self._LightLED = 20
        self._PersonAlarmLED = 19
        self._SENSOR = 26
        self._stop_sign = False
        GPIO.setup(LightLED, GPIO.OUT)
        GPIO.setup(PersonAlarmLED, GPIO.OUT)
        GPIO.setup(DHTPIN, GPIO.OUT)
        self._AlarmMoudle()

    def _turnOffLight(self):
        try:
            GPIO.output(self._LightLED, 0)
            print("turn off a light")
        except KeyboardInterrupt:
            GPIO.cleanup()

    def _turnOnLight(self):
        try:
            GPIO.output(self._LightLED, 1)
            print("turn On a light")
        except KeyboardInterrupt:
            GPIO.cleanup()

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

    def _switchAlarm(self):
        self._stop_sign = ~self._stop_sign

    def _check(self):
        return self._stop_sign

    def _AlarmMoudle(self):

        flag = False
        times = 0
        try:
            while self._check():
                # 检测人体红外是否输出低电平。若是输出低电平则表示声音被检测到，点亮关闭led
                if GPIO.input(self._SENSOR) == 1:
                    flag = not flag
                    print("有人来了")
                    GPIO.output(self._PersonAlarmLED, flag)
                times = times + 1
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
        GPIO.cleanup()
