# from datetime import date
# from typing import Optional
#
# from pydantic import BaseModel, ConfigDict
#
#
# class ProfileBase(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     username: Optional[str] = None
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     middle_name: Optional[str] = None
#     birth_date: Optional[date] = None
#
#
# class ProfileRead(ProfileBase):
#     registered_on: Optional[str]
#     id: int
#     user_id: int
#
#
# class ProfileCreate(ProfileBase):
#     pass
#
#
# class ProfileUpdate(ProfileBase):
#     pass
