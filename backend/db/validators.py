from typing import Optional

from aiohttp import web
from pydantic import BaseModel


class ImmutableModelValidator:
    def validate(self, *args, **kwargs):
        raise web.HTTPForbidden


class SeriesValidator(BaseModel):
    name: str
    year: int
    description: Optional[str]
    image_uid: Optional[str]
    creator_id: int


class SeriesItemValidator(BaseModel):
    name: str
    description: str
    identify_number: Optional[int]
    image_uid: Optional[str]
    series_id: int


class UserItemLinkValidator(BaseModel):
    user_id: int
    item_id: int
