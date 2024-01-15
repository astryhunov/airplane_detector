from flask import Flask, Response, redirect, url_for, request, jsonify, render_template, send_from_directory

import os
import cv2
import numpy as np

from ultralytics import YOLO
from PIL import Image
from werkzeug.utils import secure_filename

# from roboflow import Roboflow

model = YOLO("yolov8l.pt")

app = Flask(__name__)

def process_video(input_path, output_path):
    # Відкриваємо вхідне відео
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError("Cannot open the video")

    # Отримуємо властивості відео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # або інший кодек, залежно від формату відео

    # Створюємо об'єкт VideoWriter для запису відео
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Читаємо та обробляємо кожен кадр
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # якщо кадри завершились, виходимо з циклу

        results = model.track(frame, persist=True)
        # plot results
        processed_frame = results[0].plot()
        # Записуємо оброблений кадр
        out.write(processed_frame)

    # Закриваємо об'єкти VideoCapture та VideoWriter
    cap.release()
    out.release()

@app.route('/')
@app.route('/<filename>')
def index(filename=None):
    file_exists = False
    file_url = None
    file_type = None

    if filename:
        # Перевіряємо, чи файл дійсно існує у директорії 'static'
        file_path = os.path.join('static', filename)
        if os.path.isfile(file_path):
            file_url = url_for('static', filename=filename)
            file_exists = True
            # Визначаємо тип файлу за розширенням
            file_type = 'video' if any(filename.endswith(ext) for ext in ['.mp4', '.avi']) else 'image'

    return render_template('index.html', file_url=file_url, file_exists=file_exists, file_type=file_type)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/admin")
def admin():
    return redirect(url_for("/"))

@app.route('/detect_image', methods=['POST'])
def detect_image():
    if request.method == 'POST':

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not (file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
            return jsonify({'error': 'Invalid file format. Only JPEG files are accepted.'}), 400

        if file:
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

            # Виконання виявлення об'єктів
            results = model.predict(source=image, save=False, conf=0.15)

            # Візуалізація результатів (припускається, що results має відповідний формат)
            for r in results:
                im_array = r.plot()  # plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image

            # Конвертація зображення для відображення у відповіді
            _, buffer = cv2.imencode('.jpg', np.array(im))
            # response = Response(buffer.tobytes(), mimetype='image/jpeg')
            output_filename = 'processed_image.jpg'
            output_path = os.path.join('static', output_filename)
            im.save(output_path)
            return redirect(url_for('index', filename=output_filename))

@app.route('/detect_video', methods=['POST'])
def detect_video():
    if request.method == 'POST':
        # Отримання файлу з запиту
        file = request.files['video']

        # Перевірка, чи було вибрано файл
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not file.filename.endswith('.mp4'):
            return jsonify({'error': 'Invalid file format. Only MP4 files are accepted.'}), 400

        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join('uploads', filename)
            file.save(input_path)

            # Запускаємо обробку відео
            output_filename = 'processed_' + filename
            output_path = os.path.join('static', output_filename)
            process_video(input_path, output_path)

            return send_from_directory('static', output_filename, as_attachment=True)
            # return redirect(url_for('index', filename=output_filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
