from pydantic import BaseModel, ConfigDict, Field


class MemberResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    member_no: int = Field(alias="memberNo")
    name: str
    email: str
