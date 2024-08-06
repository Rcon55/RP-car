from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate():
    # Открываем видеопоток с камеры
    camera = cv2.VideoCapture(0)
    
    while True:
        # Захватываем кадр
        success, frame = camera.read()
        if not success:
            break
        
        # Кодируем кадр в JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Отправляем кадр как часть HTTP ответа
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
