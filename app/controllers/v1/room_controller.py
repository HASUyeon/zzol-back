from typing import List
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.response import BaseResponse
from app.schemas.room import RoomRequest, RoomResponse
from app.services.room import get_room_by_field, get_room_list, make_room_service


router = APIRouter()


@router.get("/rooms", response_model=BaseResponse[List[RoomResponse]])
def get_rooms(session: Session = Depends(get_session)):
    rooms = get_room_list(session)
    rooms_schema = [
        RoomResponse.model_validate(room, from_attributes=True).model_dump()
        for room in rooms
    ]
    response = BaseResponse(
        message_code="SUCCESS",
        message="Rooms retrieved successfully",
        result=rooms_schema,
    )
    return JSONResponse(content=jsonable_encoder(response, by_alias=True))


@router.get("/{roomNo}", response_model=BaseResponse[RoomResponse])
def get_room(roomNo: int, session: Session = Depends(get_session)):
    room = get_room_by_field(session, "room_no", roomNo)
    if not room:
        return BaseResponse(
            message_code="SUCCESS", message="Room not found", result=None
        )
    return BaseResponse(
        message_code="SUCCESS",
        message="Room retrieved successfully",
        result=RoomResponse.model_validate(room, from_attributes=True),
    )


@router.post("", response_model=BaseResponse[RoomResponse])
def make_room(request: RoomRequest, session: Session = Depends(get_session)):
    new_room = make_room_service(session, request)
    return BaseResponse(
        message_code="SUCCESS",
        message="Room maked successfully",
        result=RoomResponse.model_validate(new_room).model_dump(),
    )
