from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router as api_router
from ministry_endpoints import router as ministry_router
from tax_endpoints import router as tax_router
from connections import active_connections, manager

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://127.0.0.1:5173",  # Vite on 127.0.0.1
            "http://localhost:5173",  # Vite on localhost
            "http://localhost:8080",
            "http://localhost:8081",
            "http://localhost:8082"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app = FastAPI(title="National Financial Blockchain Administration Portal")
setup_cors(app)

# Include API routes
app.include_router(api_router, tags=["Core"])
app.include_router(ministry_router, tags=["Ministry Management"])
app.include_router(tax_router, tags=["Tax Payments"])

@app.get("/")
async def root():
    return {
        "message": "National Financial Blockchain Administration Portal API",
        "version": "2.0",
        "features": [
            "Dynamic Ministry Registration",
            "Role-Based Access Control",
            "Project Management",
            "Expense Request Workflow",
            "Blockchain-Backed Transactions",
            "Real-Time WebSocket Updates"
        ]
    }

@app.websocket("/ws/{wallet_address}")
async def websocket_endpoint(websocket: WebSocket, wallet_address: str):
    await websocket.accept()
    active_connections[wallet_address] = websocket
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive and receive messages
            data = await websocket.receive_text()
            # Echo back or process as needed
    except WebSocketDisconnect:
        # Remove the connection when the client disconnects
        manager.disconnect(websocket)
        if wallet_address in active_connections:
            del active_connections[wallet_address]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
