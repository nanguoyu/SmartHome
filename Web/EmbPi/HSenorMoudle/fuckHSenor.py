# encoding:utf-8
import random

import RPi.GPIO
import time
import os
import thread

# led的正极所在GPIO口
PersonAlarmLED = 19
# 声音传感器的out接口
SESOR = 26
# 当前led状态
RPi.GPIO.setmode(RPi.GPIO.BCM)
# 指定传感器的接口gpio26为输入模式
# 默认为高电平，低电平表示有输出
RPi.GPIO.setup(SESOR, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
# 指定GPIO19（与LED的长针）为输出模式
RPi.GPIO.setup(PersonAlarmLED, RPi.GPIO.OUT)


def AlarmMoudle():
    flag = False
    times = 0
    try:
        while True:
            # 检测人体红外是否输出低电平。若是输出低电平则表示声音被检测到，点亮关闭led
            if RPi.GPIO.input(SESOR) == random.randint(0, 1):
                if RPi.GPIO.input(SESOR) == 1:
                    flag = not flag
                    print("有人来了")
                    RPi.GPIO.output(PersonAlarmLED, flag)
                time.sleep(1)
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()
    RPi.GPIO.cleanup()


if __name__ == '__main__':
    AlarmMoudle()
