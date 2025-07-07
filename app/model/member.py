import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Member(SQLModel, table=True):
    member_no: int = Field(
        ..., alias="memberNo", primary_key=True, description="회원 번호"
    )
    email: EmailStr = Field(..., description="이메일")
    kakao_id: int = Field(..., alias="kakaoId", description="카카오 회원 번호")
    nickname: str = Field(..., min_length=1, max_length=20, description="닉네임")
    birth_date: datetime.datetime = Field(
        ..., alias="birthDate", description="생년월일"
    )
