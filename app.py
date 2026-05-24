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


@app.route('/editor')
def editor():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/layouts')
def layouts():
    return render_template('layouts.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('photos')
    layout = request.form.get('layout')
    border_color = request.form.get('border_color') or "#ffffff"

    images = []

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        images.append(Image.open(path))

    # 🎯 Layout definitions
    if layout == "strip3":
        template = [(50, 50, 300, 400), (50, 470, 300, 400), (50, 890, 300, 400)]
        canvas_size = (400, 1350)

    elif layout == "square4":
        template = [
            (50, 50, 300, 400), (370, 50, 300, 400),
            (50, 470, 300, 400), (370, 470, 300, 400)
        ]
        canvas_size = (720, 950)

    elif layout == "vertical4":
        template = [
            (50, 50, 300, 400), (50, 470, 300, 400),
            (50, 890, 300, 400), (50, 1310, 300, 400)
        ]
        canvas_size = (400, 1800)

    elif layout == "grid6":
        template = [
            (50, 50, 300, 400), (370, 50, 300, 400),
            (50, 470, 300, 400), (370, 470, 300, 400),
            (50, 890, 300, 400), (370, 890, 300, 400)
        ]
        canvas_size = (720, 1350)

    elif layout == "grid8":
        template = [
            (50, 50, 300, 400), (370, 50, 300, 400),
            (50, 470, 300, 400), (370, 470, 300, 400),
            (50, 890, 300, 400), (370, 890, 300, 400),
            (50, 1310, 300, 400), (370, 1310, 300, 400)
        ]
        canvas_size = (720, 1800)

    else:
        return "Invalid layout"

    images = images[:len(template)]

    canvas = Image.new("RGB", canvas_size, border_color)

    for img, box in zip(images, template):
        x, y, w, h = box
        img = fit_image(img, w, h)
        canvas.paste(img, (x, y))

    canvas.save(OUTPUT_PATH)

    return render_template('index.html', image_url='/static/output.png')


if __name__ == '__main__':
    app.run(debug=True)