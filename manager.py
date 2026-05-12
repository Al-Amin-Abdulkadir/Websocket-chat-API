from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.actie_connections : list[WebSocket] = []

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.actie_connections.append(websocket)
    
    def disconnect(self, websocket : WebSocket):
        self.actie_connections.remove(websocket)
    
    async def broadcast(self, message : str):
        for connection in self.actie_connections:
            await connection.send_text(message)