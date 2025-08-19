import datetime
from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    room_no: int = Field(..., alias="roomNo", primary_key=True, description="방 번호")
    room_name: str = Field(..., alias="roomName", description="방 제목")
    game_mode: str = Field(..., alias="gameMode", description="게임 모드")
    bet_mode: str = Field(..., alias="betMode", description="내기 모드")
    current_member_cnt: int = Field(
        ..., alias="currentMemberCnt", description="현재 인원 수"
    )
    max_member_cnt: int = Field(..., alias="maxMemberCnt", description="최대 인원 수")
    create_dt: datetime.datetime = Field(
        ..., alias="createDt", description="방 생성일시"
    )
    start_dt: datetime.datetime = Field(alias="startDt", description="게임 시작일시")
    end_dt: datetime.datetime = Field(alias="endDt", description="게임 종료일시")
