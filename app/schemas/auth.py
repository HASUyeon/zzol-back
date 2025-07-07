import datetime
from pydantic import EmailStr, Field

from app.model.member import Member
from app.schemas.member import MemberResponse
from app.schemas.response import CamelModel


class KakaoAccount(CamelModel):
    email: str = Field(description="카카오계정 대표 이메일")
    has_email: bool = Field(description="이메일 존재 여부(deprecated)")
    is_email_valid: bool = Field(description="이메일 유효 여부")
    is_email_verified: bool = Field(description="이메일 인증 여부")


class KakaoAccountResponse(CamelModel):
    id: int  # 카카오 회원번호
    kakao_account: KakaoAccount


class AuthTokens(CamelModel):
    access_token: str = Field()
    refresh_token: str = Field()
    grant_type: str = Field()
    expires_in: int = Field()


class KakaoSignInResponse(CamelModel):
    is_registered: bool = Field(description="회원가입을 한 회원인지 여부")
    kakao_id: int = Field(description="카카오 회원 번호")
    kakao_account: KakaoAccount = Field(description="카카오 계정 정보")
    member: MemberResponse | None = Field(description="등록된 회원")
    # token: AuthTokens | None


class KakaoSignUpRequest(CamelModel):
    kakao_id: int = Field(..., description="카카오 회원 번호")
    nickname: str = Field(..., min_length=1, max_length=20, description="닉네임")
    email: EmailStr = Field(..., description="이메일")
    birth_date: datetime.datetime = Field(..., description="생년월일")


class KakaoSignUpResponse(CamelModel):
    member: MemberResponse = Field(description="등록된 회원")
