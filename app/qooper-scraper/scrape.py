import os
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from schemas import (
    DiscussionList,
    GroupEventList,
    GroupList,
    GroupMemberList,
)
from urllib3.util import Retry


class Endpoints:
    Programs = "https://user-api.qooper.io/v1/programs"
    Groups = "https://user-api.qooper.io/v1/groups"
    GroupsJoined = "https://user-api.qooper.io/v1/groups/joined"
    Members = "https://user-api.qooper.io/v1/groups/{group_id}/members"
    GroupDiscussions = "https://user-api.qooper.io/v1/groups/{group_id}/discussions"
    GroupEventsUpcoming = (
        "https://user-api.qooper.io/v1/groups/{group_id}/events?filter=upcoming"
    )
    GroupEventsPast = (
        "https://user-api.qooper.io/v1/groups/{group_id}/events?filter=past"
    )


# region: Retrieve Token
token_path = os.getenv("QOOPER_TOKEN_PATH", "./qooper-token.txt")
try:
    with open(token_path) as f:
        qooper_token = f.read().strip()
except FileNotFoundError:
    raise FileNotFoundError(f"Token file not found at {token_path}")
except IOError:
    raise IOError(f"Error reading token file at {token_path}")
# endregion

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))
session.headers.update({"Authorization": f"Token token={qooper_token}"})

# region: Scrape Qooper
# Get all group IDs
groups = session.get(Endpoints.Groups).json()["data"]
groups_joined = session.get(Endpoints.GroupsJoined).json()["data"]
raw_groups = groups + groups_joined

print(f'All Groups: {[group['name'] for group in raw_groups]}')
print(
    f'Retrieving discussions from the following groups: {[group['name'] for group in raw_groups]}'
)


all_groups = []
for group in raw_groups:
    group = session.get(Endpoints.Groups + f'/{group["id"]}').json()["data"]
    all_groups.append(group)
all_groups = GroupList(all_groups)

# For group, get all members
all_members = []
for group in all_groups.root:
    members: list[dict] = session.get(
        Endpoints.Members.format(group_id=group.id)
    ).json()["data"]
    for member in members:
        member["group_id"] = group.id
        member["group_name"] = group.name
    all_members += members


# For group, get all discussions
# NOTE: Only gets messages from groups the token grants access to
all_discussions = []
for group in groups_joined:
    discussions: list[dict] = session.get(
        Endpoints.GroupDiscussions.format(group_id=group["id"])
    ).json()["data"]

    raw_comments = []
    # Retrieve all comments first
    for discussion in discussions:
        if len(discussion["comments"]) >= 3:
            discussion.update(
                session.get(
                    Endpoints.GroupDiscussions.format(
                        group_id=group["id"] + f'/{discussion['id']}'
                    )
                ).json()["data"]
            )

        raw_comments.extend(discussion["comments"])
        for comment in raw_comments:
            comment["is_comment"] = True
        discussion["comments"] = [comment["id"] for comment in discussion["comments"]]
        discussion["group_id"] = group["id"]
        discussion["group_name"] = group["name"]

    all_discussions += discussions
    all_discussions += raw_comments


# For group, get all events
all_events = []
for group in groups_joined:
    events: list[dict] = (
        session.get(Endpoints.GroupEventsUpcoming.format(group_id=group["id"])).json()[
            "data"
        ]
        + session.get(Endpoints.GroupEventsPast.format(group_id=group["id"])).json()[
            "data"
        ]
    )
    for event in events:
        event["group_id"] = group["id"]
        event["group_name"] = group["name"]
    all_events += events
# endregion

# region: Save output to files
file_timestamp = datetime.now().strftime(r"%Y%m%d-%H%M%S")

with open(f"output/qooper-groups-{file_timestamp}.json", "w") as groups_file:
    groups_file.write(all_groups.model_dump_json(indent=2))

with open(f"output/qooper-members-{file_timestamp}.json", "w") as members_file:
    members_file.write(GroupMemberList(all_members).model_dump_json(indent=2))

with open(f"output/qooper-discussions-{file_timestamp}.json", "w") as discussions_file:
    discussions_file.write(DiscussionList(all_discussions).model_dump_json(indent=2))

with open(f"output/qooper-events-{file_timestamp}.json", "w") as events_file:
    events_file.write(GroupEventList(all_events).model_dump_json(indent=2))
# endregion
