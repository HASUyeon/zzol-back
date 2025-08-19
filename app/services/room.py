from datetime import datetime
from venv import create
from sqlmodel import Session, select

from app.model.room import Room
from app.schemas.room import RoomRequest


def get_room_list(session: Session):
    member_list = session.exec(select(Room)).all()
    return member_list


def get_room_by_field(session: Session, field_name: str, field_value):
    try:
        field_attr = getattr(Room, field_name)
        statement = select(Room).where(field_attr == field_value)
        room = session.exec(statement).first()
        if room:
            return room
    except Exception as e:
        print("error", e)


def make_room_service(session: Session, request: RoomRequest):
    new_room = Room(
        **request.model_dump(),
        maxMemberCnt=4,
        currentMemberCnt=0,
        createDt=datetime.now(),
    )
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room
