import os
import requests
from sqlmodel import Session

from app.schemas.auth import KakaoAccountResponse, KakaoSignInResponse
from app.services.member import get_member_by_field


KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")


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


def get_kakao_member_sign_in(session: Session, code: str):
    kakao_access_token = get_kakao_access_token(code)
    kakao_member_info = get_kakao_member_info(kakao_access_token)

    member = get_member_by_field(session, "kakao_id", kakao_member_info["id"])

    if member:
        return KakaoSignInResponse(
            isRegistered=True,
            kakaoId=kakao_member_info["id"],
            kakaoAccount=kakao_member_info["kakao_account"],
            member=member,
        )
    else:
        return KakaoSignInResponse(
            isRegistered=False,
            kakaoId=kakao_member_info["id"],
            kakaoAccount=kakao_member_info["kakao_account"],
            member=None,
        )
