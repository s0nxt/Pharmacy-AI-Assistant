import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict, List, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langfuse.langchain import CallbackHandler
from agents.tools import check_inventory, check_customer_history, place_order

load_dotenv()

# Setup Langfuse
langfuse_handler = CallbackHandler()

system_rules = (
    "You are an expert pharmacist AI. Your goal is to assist customers with ordering medicines, "
    "checking their history, and providing professional advice. "
    "Follow these rules:\n"
    "1. Always check inventory before confirming an order.\n"
    "2. If a medicine requires a prescription, ask the user if they have one.\n"
    "3. Be proactive: suggest refills based on history.\n"
    "4. Use a professional tone."
)

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    customer_info: dict

tools = [check_inventory, check_customer_history, place_order]
tool_node = ToolNode(tools)

model = ChatGoogleGenerativeAI(
    model="models/gemini-flash-lite-latest", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)
model_with_tools = model.bind_tools(tools)

def call_model(state: AgentState):
    messages = state['messages']
    
    try:
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        print(f"Error invoking model: {e}")
        return {"messages": [AIMessage(content="I'm sorry, I'm having trouble connecting to my brain. Please try again.")]}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

def get_pharmacist_response(user_input: str, history: List[BaseMessage] = []):
    # Pass instructions as a HumanMessage at the beginning of the context
    messages = [HumanMessage(content=system_rules)] + history + [HumanMessage(content=user_input)]
    
    callbacks = []
    if langfuse_handler:
        callbacks.append(langfuse_handler)
        
    try:
        result = app.invoke({"messages": messages, "customer_info": {}}, config={"callbacks": callbacks})
    except Exception as e:
        print(f"Error invoking graph: {e}")
        result = app.invoke({"messages": messages, "customer_info": {}})
        
    return result['messages'][-1].content
