# encoding:utf-8
import RPi.GPIO
import time
import os

# led的正极所在GPIO口
LightLED = 19
# 声音传感器的out接口
SESOR = 26
# 当前led状态
flag = False

RPi.GPIO.setmode(RPi.GPIO.BCM)
# 指定传感器的接口gpio26为输入模式
# 默认为高电平，低电平表示有输出
RPi.GPIO.setup(SESOR, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
# 指定GPIO19（与LED的长针）为输出模式
RPi.GPIO.setup(LightLED, RPi.GPIO.OUT)


def turnOffLight():
    try:
        RPi.GPIO.output(LightLED, 0)
        print("turn off a light")
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()


def turnOnLight():
    try:
        RPi.GPIO.output(LightLED, 1)
        print("turn On a light")
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()


if __name__ == '__main__':
    try:
        turnOnLight()
        time.sleep(2)
        turnOffLight()
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()
