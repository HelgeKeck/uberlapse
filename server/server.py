import os
import subprocess
from datetime import datetime
from flask import Flask, render_template

FRAME = 0
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    global FRAME
    FRAME = 0
    return 'ok'

@app.route('/captureasync')
def captureasync():
    global FRAME
    FRAME += 1 
    os.system ('raspistill -rot 270 --saturation 5 --ISO 200 --awb greyworld --metering spot --shutter 66667 --hflip --vflip --nopreview --width 3840 --height 2160 --quality 100 --timeout 2000 --output images/' + str(FRAME).rjust(5, '0') + '.jpg')
    return 'ok'

@app.route('/capture')
def capture():
    global FRAME
    FRAME += 1 
    subprocess.Popen(['raspistill -rot 270 --saturation 5 --ISO 200 --awb greyworld --metering spot --shutter 66667 --hflip --vflip --nopreview --width 3840 --height 2160 --quality 100 --timeout 2000 --output images/' + str(FRAME).rjust(5, '0') + '.jpg'], shell=True)
    return 'ok'

@app.route('/renderasync')
def renderasync():
    FRAME = 0 
    FileName = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    print(FileName)
    os.system ('ffmpeg -filter_threads 1 -framerate 30 -pattern_type glob -i "images/*.jpg" -s:v 3840x2160 -c:v libx264 -crf 17 -pix_fmt yuv420p video/' + FileName + '.mp4')
    return 'ok'

@app.route('/render')
def render():
    FRAME = 0 
    FileName = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    print(FileName)
    subprocess.Popen(['ffmpeg -filter_threads 1 -framerate 30 -pattern_type glob -i "images/*.jpg" -s:v 3840x2160 -c:v libx264 -crf 17 -pix_fmt yuv420p video/' + FileName + '.mp4'], shell=True)
    return 'ok'

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        app.run(debug=True, host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(debug=True, host='0.0.0.0', port=9090)
