import asyncio
import json

from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.admin.crud import (
    get_first_50_messages_of_chat,
    save_message_in_admins_chat,
)
from src.helpers.databases.postgres_db.postgres_db import get_async_session
from src.helpers.response import TripNestArmeniaJSONResponse

router = APIRouter(prefix="/chats", tags=["chats"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message_to_chat(self, message: str):
        await asyncio.gather(
            *[conn.send_text(message) for conn in self.active_connections],
            return_exceptions=True
        )


chat_manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_async_session),
):
    await chat_manager.connect(websocket)
    data_dict = {}
    try:
        while True:
            raw = await websocket.receive_text()
            data_dict = json.loads(raw)

            await save_message_in_admins_chat(
                db=db,
                admin_id=data_dict["adminId"],
                message=data_dict["message"],
            )

            await chat_manager.send_message_to_chat(raw)

    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        # Безопасно строим имя — если нет, просто “A user”
        name = (
            f"{data_dict.get('firstName','')} {data_dict.get('lastName','')}"
        ).strip() or "A user"
        await chat_manager.send_message_to_chat(
            json.dumps({"system": f"{name} left the chat"})
        )


@router.get("/get-first-50-messages")
async def get_first_50_messages(db: AsyncSession = Depends(get_async_session)):
    messages = await get_first_50_messages_of_chat(db)
    print(TripNestArmeniaJSONResponse(content={"messages_list": messages}).__dict__)
    return TripNestArmeniaJSONResponse(content={"messages_list": messages})
