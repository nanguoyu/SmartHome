import os

os.system("sudo modprobe bcm2835-v4l2")


def capturePhoto():
    os.system("curl -o /home/pi/SmartHome/Web/static/1.jpg 192.168.2.242:8090/?action=snapshot")
    print("you can find 1.jpg in /home/pi/SmartHome/Web/static/1.jpg")
    return "you can find 1.jpg in /home/pi/SmartHome/Web/static/1.jpg"


if __name__ == '__main__':
    capturePhoto()
