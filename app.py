from flask import Flask, render_template, request
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_PATH = 'static/output.png'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 🧠 Smart crop (no stretching)
def fit_image(img, target_w, target_h):
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))

    return img.resize((target_w, target_h))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/layouts')
def layouts():
    return render_template('layouts.html')


if __name__ == '__main__':
    app.run(debug=True)