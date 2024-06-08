import asyncio
import websockets
import requests

async def handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
            if data == "Activate Cam":
                url = "https://lab-moving-grizzly.ngrok-free.app/api/model/predict_image_from_esp32/"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        json_data = response.json()
                        predict_result = json_data.get("predict_result")
                        if predict_result:
                            await websocket.send(predict_result)
                        else:
                            await websocket.send("Không tìm thấy predict_result trong JSON")
                    else:
                        await websocket.send(f"Lỗi khi gửi yêu cầu GET, mã trạng thái: {response.status_code}")
                except Exception as e:
                    await websocket.send(f"Lỗi khi gửi yêu cầu GET: {str(e)}")
        except websockets.ConnectionClosed:
            break

start_server = websockets.serve(handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
