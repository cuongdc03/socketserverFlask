from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Mở kết nối WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Nhận dữ liệu từ client (ESP8266)
        data = await websocket.receive_text()
        
        # Nếu nhận được dữ liệu từ ESP8266
        if data == "Activate Cam":
            # Gửi yêu cầu GET đến URL mong muốn
            url = "https://lab-moving-grizzly.ngrok-free.app/api/model/predict_image_from_esp32/"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Xử lý dữ liệu JSON nhận được từ URL
                    json_data = response.json()
                    predict_result = json_data.get("predict_result")
                    if predict_result:
                        # Gửi giá trị của key "predict_result" qua kết nối WebSocket
                        await websocket.send_text(predict_result)
                    else:
                        await websocket.send_text("Không tìm thấy predict_result trong JSON")
                else:
                    await websocket.send_text(f"Lỗi khi gửi yêu cầu GET, mã trạng thái: {response.status_code}")
            except Exception as e:
                await websocket.send_text(f"Lỗi khi gửi yêu cầu GET: {str(e)}")

# Thực hiện các hoạt động khác của FastAPI