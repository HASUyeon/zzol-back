from typing import Optional

from sqlmodel import Field, SQLModel


class Member(SQLModel, table=True):
    member_no: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field()
    kakao_id: str
