from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.db.database import get_session
from app.model.member import Member
from app.schemas.member import MemberResponse
from app.schemas.response import BaseResponse

router = APIRouter()


@router.get("/members", response_model=BaseResponse[List[MemberResponse]])
def get_members(session: Session = Depends(get_session)):
    members = session.exec(select(Member)).all()
    members_schema = [
        MemberResponse.model_validate(member, from_attributes=True)
        for member in members
    ]
    response = BaseResponse(
        messageCode="SUCCESS",
        message="Members retrieved successfully",
        result=members_schema,
    )
    return JSONResponse(content=jsonable_encoder(response, by_alias=True))


@router.get("/{memberNo}", response_model=BaseResponse[MemberResponse])
def get_member(memberNo: int, session: Session = Depends(get_session)):
    statement = select(Member).where(Member.member_no == memberNo)
    member = session.exec(statement).first()
    if not member:
        return BaseResponse(
            messageCode="SUCCESS", message="Member not found", result=None
        )
    return BaseResponse(
        messageCode="SUCCESS",
        message="Members retrieved successfully",
        result=MemberResponse.model_validate(member, from_attributes=True),
    )
