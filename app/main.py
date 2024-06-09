from fastapi import FastAPI, WebSocket
import requests

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        
        if data == "Activate Cam":
            url = "https://lab-moving-grizzly.ngrok-free.app/api/model/predict_image_from_esp32/"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    json_data = response.json()
                    predict_result = json_data.get("predict_result")
                    if predict_result:
                        await websocket.send_text(predict_result)
                    else:
                        await websocket.send_text("Không tìm thấy predict_result trong JSON")
                else:
                    await websocket.send_text(f"Lỗi khi gửi yêu cầu GET, mã trạng thái: {response.status_code}")
            except Exception as e:
                await websocket.send_text(f"Lỗi khi gửi yêu cầu GET: {str(e)}")
