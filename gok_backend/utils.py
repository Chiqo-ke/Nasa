# utils.py

async def notify_user(wallet_address: str, message: str, active_connections: dict):
    """Send a notification to a specific user."""
    if wallet_address in active_connections:
        websocket = active_connections[wallet_address]
        await websocket.send_text(message)