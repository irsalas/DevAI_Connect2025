import os
from typing import TypedDict, List, Union, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from operator import add as add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from numpy import dot
from tools.customer_tools import get_customer_services_tool
from tools.nso_tools import (
    get_service_parameters, execute_ping, check_if_status,
    check_mp_bgp_session_status, check_rt_configuration, check_route_availability
)
from tools.rag_tools import retrieve_tool


# Define agent state and tools
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

llm = ChatOpenAI(model="gpt-4o", temperature=0)
#llm = ChatOllama(model="llama3.1:8b", temperature=0, base_url=("http://")) #bad
#llm = ChatOllama(model="gpt-oss:20b", temperature=0, base_url=("http://")) #good
#llm = ChatOllama(model="gpt-oss:20b", temperature=0, base_url=("http://")) #good
#llm = ChatOllama(model="mistral-nemo:12b", temperature=0, base_url=("http://")) #better

tools = [
    get_customer_services_tool, get_service_parameters, 
    execute_ping, check_if_status, retrieve_tool, 
    check_mp_bgp_session_status, check_route_availability,
    check_rt_configuration
]

llm = llm.bind_tools(tools)
tools_dict = {our_tool.name: our_tool for our_tool in tools}

# System prompt
system_prompt = """
You are an intelligent AI assistant acting as network engineer. Your main concern is to troubleshoot MPLS L3VPN issues.
For troubleshooting MPLS L3VPN issues, you have access to a variety of tools and resources.
You can use these tools to gather information, run diagnostics, and provide solutions to common problems.
You strictly must follow the steps outlined in the l3vpn troubleshooting guide, you can access it using the "retrieve_tool".
Before you start troubleshooting, you must gather **ALL** the steps detailed in the l3vpn troubleshooting guide.
You should always cite the specific parts of the documents you use in your logic to solve problems.
In your conclusion you must include all the steps and the intermediate results.
"""

def should_continue(state: AgentState) -> str:
    """Check if the last message contains tool calls"""
    result = state["messages"][-1]
    if hasattr(result, "tool_calls") and len(result.tool_calls) > 0:
        return "continue"
    else:
        return "end"

def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state."""
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    #print(message)
    return {'messages': [message]}

def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with: {t['args']}")
        
        if t['name'] not in tools_dict:
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        else:
            result = tools_dict[t['name']].invoke(t['args'])
            print(f"Result length: {len(str(result))}")
        
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
    
    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}

# Build the LangGraph
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("llm", call_llm)
    graph.add_node("retriever_agent", take_action)
    graph.add_conditional_edges("llm", should_continue, {"continue": "retriever_agent", "end": END})
    graph.add_edge("retriever_agent", "llm")
    graph.set_entry_point("llm")
    app = graph.compile()
    return app