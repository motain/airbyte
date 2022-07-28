import requests
from typing import Any, Mapping, Iterable, Optional

from airbyte_cdk.sources.streams.http import HttpStream


class DiscordServerPreviewStream(HttpStream):
    url_base = "https://discord.com"
    primary_key = ""
    
    def __init__(self, config: Mapping[str, Any], **_):
        super().__init__()
        self.guild_id = config["guild_id"]
        self.server_token = config["server_token"]

    def request_headers(self, **_) -> Mapping[str, Any]:
        return {'Authorization': "Bot " + self.server_token}

    def parse_response(self, response: requests.Response, **_) -> Iterable[Mapping]:
        yield from [response.json()]

    def next_page_token(self, _) -> Optional[Mapping[str, Any]]:
        return None


class ServerPreview(DiscordServerPreviewStream):
    def path(self, **_) -> str:
        return "api/guilds/{}/preview".format(self.guild_id)
