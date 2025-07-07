from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.model.member import Member
from app.schemas.auth import (
    KakaoSignInResponse,
    KakaoSignUpRequest,
    KakaoSignUpResponse,
)
from app.schemas.member import MemberResponse
from app.schemas.response import BaseResponse
from app.services.auth import get_kakao_member_sign_in, post_kakao_sign_up


router = APIRouter()


@router.get("/sign-in/kakao", response_model=BaseResponse[KakaoSignInResponse])
def sign_in_kakao(code: str, session: Session = Depends(get_session)):
    response = get_kakao_member_sign_in(session, code)
    return BaseResponse(
        message_code="SUCCESS",
        message="조회 성공",
        result=response,
    )


@router.post("/sign-up/kakao", response_model=BaseResponse[KakaoSignUpResponse])
def sign_up_kakao(request: KakaoSignUpRequest, session: Session = Depends(get_session)):
    new_member = post_kakao_sign_up(session, request)
    return BaseResponse(
        message_code="SUCCESS",
        message="등록 성공",
        result=KakaoSignUpResponse(member=MemberResponse(**new_member.model_dump())),
    )
