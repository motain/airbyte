import json
import time
import requests
import datetime
from typing import Any, Mapping, Iterable, Optional, MutableMapping

from airbyte_cdk.sources.streams.http import HttpStream


class EventsStream(HttpStream):
  primary_key = "id"
  cursor_field = "id"
  page_size = 100
  page = 1
  interrupt_execution = False
  url_base = "https://prod-main-net-dashboard-api.azurewebsites.net"
    
  def __init__(self, config: Mapping[str, Any], event_id: str, **_):
    super().__init__()
    self.event_id = event_id
    self.company_id = config["company_id"]
    self._cursor_value = ""

  def request_headers(self, **_) -> Mapping[str, Any]:
    return {}

  def request_params(self, **_) -> MutableMapping[str, Any]:
    return {
      "page": self.page,
      "eventType": self.event_id,
      "pageSize": self.page_size,
    }

  def parse_response(self, response: requests.Response, **_) -> Iterable[Mapping]:
    print("############################# Extracting")
    print("#############################" + response.request.url)
    print("#############################")

    if len(response.json()) < self.page_size:
      self.interrupt_execution = True

    yield from json.loads(json.dumps(response.json()).lower())

  def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:

    if len(response.json()) == 0:
      return None

    if self.page == 1:
      self._cursor_value = response.json()[0]["id"]

    if self.interrupt_execution:
      return None

    self.page = self.page + 1
    return {
      "page": self.page,
      "eventType": self.event_id,
      "pageSize": self.page_size,
    }

  def read_records(self, *args, **kwargs) -> Iterable[Mapping[str, Any]]:
    for record in super().read_records(*args, **kwargs):
      if record["id"] == self._cursor_value:
        self.interrupt_execution = True
        return None
      yield record

  @property
  def state(self) -> Mapping[str, Any]:
    return {self.cursor_field: self._cursor_value}

  @state.setter
  def state(self, value: Mapping[str, Any]):
    self.page = 1
    self.interrupt_execution = False
    self._cursor_value = value["id"]


class CreatedEvents(EventsStream):
  def path(self, **_) -> str:
    return f"api/company/{self.company_id}/search"


class RemovedEvents(EventsStream):
  def path(self, **_) -> str:
    return f"api/company/{self.company_id}/search"
