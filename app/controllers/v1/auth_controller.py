from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.auth import KakaoSignInResponse
from app.schemas.response import BaseResponse
from app.services.auth import get_kakao_member_sign_in


router = APIRouter()


@router.get("/sign-in/kakao", response_model=BaseResponse[KakaoSignInResponse])
def sign_in_kakao(code: str, session: Session = Depends(get_session)):
    response = get_kakao_member_sign_in(session, code)
    return BaseResponse(
        messageCode="SUCCESS",
        message="조회 성공",
        result=KakaoSignInResponse.model_validate(response, from_attributes=True),
    )
