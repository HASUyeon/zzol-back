from sqlmodel import Session, select

from app.model.member import Member
from app.schemas.response import BaseResponse


def get_member_list(session: Session):
    member_list = session.exec(select(Member)).all()
    return member_list


def get_member_by_field(session: Session, field_name: str, field_value):
    try:
        field_attr = getattr(Member, field_name)
        statement = select(Member).where(field_attr == field_value)
        member = session.exec(statement).first()
        if member:
            return member
    except Exception as e:
        print("error", e)
