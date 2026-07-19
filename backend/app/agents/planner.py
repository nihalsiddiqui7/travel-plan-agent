from langchain_core.messages import AIMessage
from app.graph.state import TravelState


def planner_node(state: TravelState) -> TravelState:
    """
    First Planner Node.
    For now, it just replies with a static message.
    """

    return {
        "messages": [
            AIMessage(
                content="Hello! I'm your AI Travel Planner. How can I help you today?"
            )
        ],
        "final_response": "Hello! I'm your AI Travel Planner. How can I help you today.",
    }