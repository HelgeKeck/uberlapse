import os
import subprocess
from datetime import datetime
from flask import Flask, render_template

FRAME = 0
FOLDER = ""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    global FOLDER
    global FRAME
    FRAME = 0

    # Mode
    MODE = 0o666

    # Root Folder
    ROOT_FOLDER = '/home/pi/uberlapse/server/images'

    # Project Folder
    FOLDER = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    # Create Folder
    os.mkdir(os.path.join(ROOT_FOLDER, FOLDER))
    return 'ok'

@app.route('/captureasync')
def captureasync():
    global FOLDER
    if FOLDER != '':
        global FRAME
        FRAME += 1 
        os.system ('raspistill --saturation 5 --ISO 400 --awb shade --metering spot --shutter 33333 --flicker 50hz --rotation 180 --nopreview --width 3840 --height 2160 --quality 100 --timeout 2000 --output images/' + FOLDER + '/' + str(FRAME).rjust(5, '0') + '.jpg')
        return 'ok'
    return 'error'

@app.route('/capture')
def capture():
    global FOLDER
    if FOLDER != '':
        global FRAME
        FRAME += 1 
        # subprocess.Popen(['raspistill --saturation 5 --ISO 400 --awb shade --metering spot --shutter 33333 --flicker 50hz --rotation 180 --nopreview --width 3840 --height 2160 --quality 100 --timeout 2000 --output images/' + FOLDER + '/' + str(FRAME).rjust(5, '0') + '.jpg'], shell=True)
        subprocess.Popen(['libcamera-still --width 3840 --height 2160 -n 1 -q 100 -o images/' + FOLDER + '/' + str(FRAME).rjust(5, '0') + '.jpg'], shell=True)
        return 'ok'
    return 'error'

@app.route('/renderasync')
def renderasync():
    global FOLDER
    if FOLDER != '':
        os.system ('ffmpeg -framerate 30 -pattern_type glob -i "images/' + FOLDER + '/*.jpg" -s:v 3840x2160 -c:v libx264 -crf 17 -pix_fmt yuv420p video/' + FOLDER + '.mp4')
        return 'ok'
    return 'error'

@app.route('/render')
def render():
    global FOLDER
    if FOLDER != '':
        subprocess.Popen(['ffmpeg -framerate 30 -pattern_type glob -i "images/' + FOLDER + '/*.jpg" -s:v 3840x2160 -c:v libx264 -crf 17 -pix_fmt yuv420p video/' + FOLDER + '.mp4'], shell=True)
        return 'ok'
    return 'error'

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        app.run(debug=True, host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(debug=True, host='0.0.0.0', port=9090)
