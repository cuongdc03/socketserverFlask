from flask import Flask
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    if data == "Activate Cam":
        url = "https://lab-moving-grizzly.ngrok-free.app/api/model/predict_image_from_esp32/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                predict_result = json_data.get("predict_result")
                if predict_result:
                    emit('response', predict_result)
                else:
                    emit('response', "Không tìm thấy predict_result trong JSON")
            else:
                emit('response', f"Lỗi khi gửi yêu cầu GET, mã trạng thái: {response.status_code}")
        except Exception as e:
            emit('response', f"Lỗi khi gửi yêu cầu GET: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
