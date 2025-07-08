from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.member import MemberResponse
from app.schemas.response import BaseResponse
from app.services.auth import get_member_by_access_token
from app.services.member import get_member_by_field, get_member_list

router = APIRouter()


@router.get("/me", response_model=BaseResponse[MemberResponse])
def get_my_info(member=Depends(get_member_by_access_token)):
    return BaseResponse(
        message_code="SUCCESS",
        message="Members retrieved successfully",
        result=MemberResponse(**member.model_dump()),
    )


@router.get("/members", response_model=BaseResponse[List[MemberResponse]])
def get_members(session: Session = Depends(get_session)):
    members = get_member_list(session)
    members_schema = [
        MemberResponse.model_validate(members, from_attributes=True)
        for member in members
    ]
    response = BaseResponse(
        message_code="SUCCESS",
        message="Members retrieved successfully",
        result=members_schema,
    )
    return JSONResponse(content=jsonable_encoder(response, by_alias=True))


@router.get("/{memberNo}", response_model=BaseResponse[MemberResponse])
def get_member(memberNo: int, session: Session = Depends(get_session)):
    member = get_member_by_field(session, "member_no", memberNo)
    if not member:
        return BaseResponse(
            message_code="SUCCESS", message="Member not found", result=None
        )
    return BaseResponse(
        message_code="SUCCESS",
        message="Members retrieved successfully",
        result=MemberResponse.model_validate(member, from_attributes=True),
    )
