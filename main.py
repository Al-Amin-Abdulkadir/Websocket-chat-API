from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from manager import ConnectionManager
from fastapi.responses import FileResponse

app = FastAPI()
manager = ConnectionManager()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket : WebSocket, client_id : int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id} : {data}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"client {client_id} left the chat")


@app.get("/chat")
async def get():
    return FileResponse("static/UI.html")