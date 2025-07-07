import datetime

from sqlmodel import Field

from app.schemas.response import CamelModel


class MemberResponse(CamelModel):
    member_no: int = Field(..., primary_key=True, description="회원 번호")
    email: str = Field(..., description="이메일")
    kakao_id: int = Field(..., description="카카오 회원 번호")
    nickname: str = Field(..., min_length=1, max_length=20, description="닉네임")
    birth_date: datetime.datetime = Field(
        ..., alias="birthDate", description="생년월일"
    )
