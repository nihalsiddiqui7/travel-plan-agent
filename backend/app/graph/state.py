from typing import Annotated

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class TravelState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    user_request: str

    destination: str | None
    days: int | None
    budget: int | None

    itinerary: str | None

    final_response: str | None