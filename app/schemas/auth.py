from pydantic import BaseModel, Field

from app.model.member import Member


class KakaoAccount(BaseModel):
    email: str
    has_email: bool
    is_email_valid: bool
    is_email_verified: bool


class KakaoAccountResponse(BaseModel):
    id: int  # 카카오 회원번호
    kakao_account: KakaoAccount


class AuthTokens(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    grant_type: str = Field(alias="grantType")
    expires_in: int = Field(alias="expiresIn")


class KakaoSignInResponse(BaseModel):
    is_registered: bool = Field(alias="isRegistered")  # 회원가입을 한 회원인지 여부
    kakao_id: str = Field(alias="kakaoId")
    kakao_account: KakaoAccount = Field(alias="kakaoAccount")
    member: Member | None
    # token: AuthTokens | None
