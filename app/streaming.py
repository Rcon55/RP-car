from flask import Flask, Response
from picamera import PiCamera
from io import BytesIO

app = Flask(__name__)
camera = PiCamera()

def generate():
    with BytesIO() as stream:
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Откатываем позицию начала буфера
            stream.seek(0)
            # Читаем данные из потока
            frame = stream.read()
            # Отправляем данные как часть HTTP ответа
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # Сбрасываем позицию в начале для следующего кадра
            stream.seek(0)
            stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera.start_preview()
    app.run(host='0.0.0.0', port=5000, debug=True)
