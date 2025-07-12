from datetime import datetime, timedelta
from enum import member
import os
from typing import Annotated
from fastapi import Depends, HTTPException, Header
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
import requests
from sqlmodel import Session

from app.db.database import get_session
from app.model.member import Member
from app.schemas.auth import (
    KakaoSignInResponse,
    KakaoSignUpRequest,
    KakaoSignUpResponse,
)
from app.schemas.member import MemberResponse
from app.services.member import get_member_by_field
from jose import JWTError, jwt


KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_ALGORITHM = os.getenv("ACCESS_TOKEN_ALGORITHM")
auth_header = APIKeyHeader(name="Authorization", auto_error=False)

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
)


def get_kakao_access_token(code: str):
    try:
        token_url = f"https://kauth.kakao.com/oauth/token?client_id={KAKAO_REST_API_KEY}&client_secret={KAKAO_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={KAKAO_REDIRECT_URI}"
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        token_response = requests.post(token_url, headers=headers)

        print("token_response", token_response)

        if token_response.status_code != 200:
            raise Exception

        kakao_access_token = token_response.json()["access_token"]
        return kakao_access_token
    except Exception as e:
        print("error", e)
        raise Exception("get_kakao_access_token error")


def get_kakao_member_info(kakao_access_token: str):
    try:
        member_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": "Bearer " + kakao_access_token,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        member_info_response = requests.get(member_info_url, headers=headers)
        if member_info_response.status_code != 200:
            raise Exception
        kakao_member_info = member_info_response.json()
        print("kakao_member_info", kakao_member_info)
        return kakao_member_info
    except Exception as e:
        print("error", e)
        raise Exception("get_kakao_member_info error")


def create_access_token(member: Member):
    if member and ACCESS_TOKEN_SECRET_KEY and ACCESS_TOKEN_ALGORITHM:
        data = {
            "sub": str(member.member_no),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        access_token = jwt.encode(
            data, key=ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
        )
        return access_token


def get_access_token_by_header(header_value: str = Depends(auth_header)):
    if not header_value or not header_value.startswith("Bearer "):
        raise credentials_exception
    return header_value.replace("Bearer ", "")


def get_member_by_access_token(
    session: Session = Depends(get_session),
    access_token: str = Depends(get_access_token_by_header),
):
    if access_token and ACCESS_TOKEN_SECRET_KEY and ACCESS_TOKEN_ALGORITHM:
        try:
            payload = jwt.decode(
                token=access_token,
                key=ACCESS_TOKEN_SECRET_KEY,
                algorithms=[ACCESS_TOKEN_ALGORITHM],
            )
            member_no = payload.get("sub")
            if member_no is None:
                raise credentials_exception
        except JWTError as error:
            print(error)
            raise credentials_exception

        member = get_member_by_field(
            session, field_name="member_no", field_value=member_no
        )
        if member is None:
            raise credentials_exception
        return member
    raise credentials_exception


def get_kakao_member_sign_in(session: Session, code: str):
    kakao_access_token = get_kakao_access_token(code)
    kakao_member_info = get_kakao_member_info(kakao_access_token)

    member = get_member_by_field(session, "kakao_id", kakao_member_info["id"])

    if member:
        return KakaoSignInResponse(
            is_registered=True,
            kakao_id=kakao_member_info["id"],
            kakao_account=kakao_member_info["kakao_account"],
            member=MemberResponse(**member.model_dump()),
            access_token=create_access_token(member),
        )
    else:
        return KakaoSignInResponse(
            is_registered=False,
            kakao_id=kakao_member_info["id"],
            kakao_account=kakao_member_info["kakao_account"],
            member=None,
        )


def post_kakao_sign_up(session: Session, request: KakaoSignUpRequest):
    existed_member = get_member_by_field(session, "kakao_id", request.kakao_id)
    if existed_member:
        raise HTTPException(status_code=409, detail="이미 등록된 회원입니다.")
    new_member = Member(**request.model_dump())
    session.add(new_member)
    session.commit()
    session.refresh(new_member)
    return KakaoSignUpResponse(
        member=MemberResponse(**new_member.model_dump()),
        access_token=create_access_token(new_member),
    )
