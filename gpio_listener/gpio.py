import requests
import RPi.GPIO as gpio
from time import sleep


FRAME_PIN = 21
RESET_PIN = 22
RENDER_PIN = 23

ENDPOINT = 'http://192.168.0.199:9090'


def setup():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    gpio.setup(FRAME_PIN, gpio.OUT)
    gpio.setup(RESET_PIN, gpio.OUT)
    gpio.setup(RENDER_PIN, gpio.OUT)

    gpio.output(FRAME_PIN, gpio.LOW)
    gpio.output(RESET_PIN, gpio.LOW)

    print('Uberlapse GPIO listener...')
    print('FRAME_PIN  = ' + str(FRAME_PIN))
    print('RESET_PIN  = ' + str(RESET_PIN))
    print('RENDER_PIN = ' + str(RENDER_PIN))


def loop():
    while True: 
        frame_state = gpio.input(FRAME_PIN)
        if frame_state:
            print('taking snapshot...')
            response = requests.get(ENDPOINT + '/capture', data='')
            if (response.ok):
                print('ok')
            else:
                print('error')
            gpio.output(FRAME_PIN, gpio.LOW)
        else:
            reset_state = gpio.input(RESET_PIN)
            if reset_state:
                print('reset...')
                response = requests.get(ENDPOINT + '/reset', data='')
                if (response.ok):
                    print('ok')
                else:
                    print('error')
                gpio.output(FRAME_PIN, gpio.LOW)
            else:
                render_state = gpio.input(RENDER_PIN)
                if render_state:
                    print('rendering...')
                    response = requests.get(ENDPOINT + '/render', data='')
                    if (response.ok):
                        print('ok')
                    else:
                        print('error')
                    gpio.output(RENDER_PIN, gpio.LOW)
        sleep(0.5)


setup()
loop()
