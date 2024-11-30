from pydantic import BaseModel, RootModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class Group(BaseModel, Generic[T]):
    id: int
    name: str
    description: Optional[str] = ""
    image_url: Optional[str]
    kind: str
    tags: list[str] = []
    is_joined: bool = True
    members_count: int = 0
    resources_count: int = 0
    discussions_count: int = 0
    past_events_count: int = 0
    upcoming_events_count: int = 0
    created_at: str


class GroupList(RootModel):
    root: list[Group]


class GroupMember(BaseModel, Generic[T]):
    id: int
    first_name: str
    last_name: str
    image_url: Optional[str]
    current_position: Optional[str]
    current_organization: Optional[str]
    roles: list[str] = []


class GroupMemberList(RootModel):
    root: list[GroupMember]


class GroupEvent(BaseModel, Generic[T]):
    id: int
    title: str
    timezone: str
    start_time: str
    end_time: str
    image_url: Optional[str]
    updated_at: str
    created_at: str
    address: Optional[str]
    # When scraping discussions or events,
    # store their publishers in a separate group member table,
    # Then keep only the ID on the relevant record
    publisher: GroupMember["id"]


class GroupEventList(RootModel):
    root: list[GroupEvent]


class Discussion(BaseModel, Generic[T]):
    id: int
    # If comments_count > 2,
    # query the discussion detail page to get all comments
    comments_count: Optional[int] = None
    upvotes_count: Optional[int] = None
    attachments_count: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: str
    publisher: GroupMember["id"]
    tags: list[str] = []
    upvotes_user_ids: list[int] = []
    comments: list[int] = []
    is_comment: bool = False


class DiscussionList(RootModel):
    root: list[Discussion]
