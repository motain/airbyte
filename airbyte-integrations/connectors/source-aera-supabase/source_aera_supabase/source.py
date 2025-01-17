import requests
from typing import Any, Mapping, Tuple, List
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream

from .streams import (
    Users
)

class SourceFindSupabase(AbstractSource):

    def check_connection(self, _, config) -> Tuple[bool, str]:
        base_url = config["project_url"]
        anon_public_key = config["anon_public_key"]
        headers = {
            "apikey": anon_public_key,
            "Authorization": f"Bearer {anon_public_key}"
        }
        params = {
            "limit": 10, "offset": 0
        }
        url = f"{base_url}/rest/v1/unpacked_items"
        response = requests.get(url, headers=headers, params=params)
        if len(response.json()) == 10:
            return True, "accepted"
        else:
            return False, "error"


    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        return [
            Users(config, "unpacked_items")
        ]
