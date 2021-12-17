import requests
import RPi.GPIO as gpio
from time import sleep

FRAME_PIN = 21
RESET_PIN = 22
RENDER_PIN = 23

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(FRAME_PIN, gpio.OUT)
gpio.setup(RESET_PIN, gpio.OUT)
gpio.setup(RENDER_PIN, gpio.OUT)

gpio.output(FRAME_PIN, gpio.LOW)
gpio.output(RESET_PIN, gpio.LOW)

print('uberlapse gpio listener running...')
while True: 
    frame_state = gpio.input(FRAME_PIN)
    if frame_state:
        print('taking snapshot...')
        response = requests.get('http://192.168.0.199:9090/captureasync', data='')
        if (response.ok):
            print('ok')
        else:
            print('error')
        gpio.output(FRAME_PIN, gpio.LOW)
    else:
        reset_state = gpio.input(RESET_PIN)
        if reset_state:
            print('reset...')
            response = requests.get('http://192.168.0.199:9090/reset', data='')
            if (response.ok):
                print('ok')
            else:
                print('error')
            gpio.output(FRAME_PIN, gpio.LOW)
        else:
            render_state = gpio.input(RENDER_PIN)
            if render_state:
                print('rendering...')
                response = requests.get('http://192.168.0.199:9090/render', data='')
                if (response.ok):
                    print('ok')
                else:
                    print('error')
                gpio.output(RENDER_PIN, gpio.LOW)
    sleep(0.5)
