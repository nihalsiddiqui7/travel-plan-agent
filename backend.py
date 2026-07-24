import os
from dotenv import load_dotenv
import requests
from typing import TypedDict,Annotated
import operator
import uuid
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    AnyMessage
)
from langchain_openai import ChatOpenAI
from tools.flight_tool import search_flights
from tools.tavily_tool import tavily_search



os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
if os.getenv("LANGSMITH_PROJECT"):
    os.environ.setdefault("LANGCHAIN_PROJECT", os.getenv("LANGSMITH_PROJECT"))


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the environment variables.")

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"
    return database_url


#======================
# LLM SETUP
#======================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.2,
)

#===========================================================================


#=====================
# STATE
#====================

class TravelPlanState(TypedDict):
    messages: Annotated[list[AnyMessage],operator.add,"The conversation history between the user and the agent."]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

#===========================================================================

#====================
#FLIGHT AGENT
#====================

def flight_agent(state: TravelPlanState):
    """
    Flight agent that searches for flights based on the user's query.

    Args:
        state (TravelPlanState): The current state of the conversation."""

    user_query = state["user_query"]
    flight_results = search_flights(user_query)


    return {
        "flight_results": flight_results,
        "messages": [
            AIMessage(content="Flight search completed.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

#========================================================


#========================
#HOTEL AGENT
#========================

def hotel_agent(state: TravelPlanState):
    """
    Hotel agent that searches for hotels based on the user's query.

    Args:
        state (TravelPlanState): The current state of the conversation."""

    query = f'Best Hotel for {state["user_query"]}'
    hotel_results = tavily_search(query)


    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel search completed.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

#========================================================

#========================
#ITINERARY AGENT
#========================

def itinerary_agent(state: TravelPlanState):
    """
    Itinerary agent that generates a travel itinerary based on the user's query and search results.

    Args:
        state (TravelPlanState): The current state of the conversation.""" 

    itinerary_prompt = f"""
    You are a travel itinerary generator. Based on the user's query and the search results for flights and hotels, generate a detailed travel itinerary.
    Make it informative, engaging, and easy to follow. Include recommendations for activities, dining, and sightseeing based on the user's query.
    User Query: {state["user_query"]}

    Flight Results: {state["flight_results"]}

    Hotel Results: {state["hotel_results"]}

    Please generate a detailed travel itinerary based on the above information.
    """

    response = llm.invoke([
        SystemMessage(content="You are a helpful travel itinerary generator."),
        HumanMessage(content=itinerary_prompt)
    ])
    
    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


#========================================================

#========================
#FINAL RESPONSE AGENT
#========================

def final_response_agent(state: TravelPlanState):
    """
    Final response agent that compiles the final response to the user based on the itinerary generated.

    Args:
        state (TravelPlanState): The current state of the conversation."""

    final_response_prompt = f"""
    You are a travel assistant. Based on the user's query and the generated itinerary, compile a final response to the user.
    Make it concise, informative, and engaging.Format the response in the following way:
    Format the response in the following way:
    1:Travel Plan Summary
    2:Flight Details
    3:Hotel Details
    4:Itinerary Overview
    5:Additional Recommendations
    6:Closing Remarks

    User Query: {state["user_query"]}

    Itinerary: {state["itinerary"]}

    Please compile a final response to the user based on the above information.
    """

    response = llm.ainvoke([
        SystemMessage(content="You are a helpful travel assistant."),
        HumanMessage(content=final_response_prompt)
    ])
    
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


graph = StateGraph(TravelPlanState)
#Nodes
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
# graph.add_node("final_response_agent", final_response_agent)

#Edges
graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", END)
# graph.add_edge("final_response_agent", END)

#=============================================


#========================
#POSTGRES CHECKPOINT SAVER
#=======================

DATABASE_URL = get_database_url()

_conn = psycopg.connect(DATABASE_URL,
                        autocommit=True, 
                        row_factory=dict_row)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()


travelgraph = graph.compile(
    checkpointer=checkpointer,
)


#=========================
#Run the travel plan agent
#========================

def run_travel_plan_agent(user_query: str,thread_id: str | None = None):
    if thread_id is None:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable":{
            "thread_id": thread_id
        }
    }
    result =travelgraph.invoke(
        {
            "messages":[HumanMessage(content=user_query)],
            "user_query": user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    final_result = result["messages"][-1].content

    return {
        "thread_id": thread_id,
        "final_result": final_result,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0)
    }




# if __name__ == "__main__":
#     user_query = input("Enter your travel-related query: ")
#     result = run_travel_plan_agent(user_query)
#     print("\nFinal Result:\n")
#     print(result["final_result"])