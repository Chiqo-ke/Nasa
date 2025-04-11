from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router as api_router
from connections import active_connections

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app = FastAPI()
setup_cors(app)

# Include API routes
app.include_router(api_router)

@app.websocket("/ws/{wallet_address}")
async def websocket_endpoint(websocket: WebSocket, wallet_address: str):
    await websocket.accept()
    active_connections[wallet_address] = websocket
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove the connection when the client disconnects
        del active_connections[wallet_address]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
