from typing import TypedDict ,Annotated,List
import operator
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
import os
from langchain_core.tools import tool 
from langgraph.prebuilt import ToolNode ,tools_condition
from langchain_core.messages import HumanMessage , AIMessage
from core.news_harvester import NewsHarvester
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver 

class SwarmState(TypedDict):
    messages : Annotated[List,operator.add]
    next_agent :str

hf_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN","paste the api key here")
llm = HuggingFaceEndpoint(
        repo_id = "choose by yourself ",
        task = "text-generation",
        max_new_tokens= 512,
        temperature = 0.1,
        huggingfacehub_api_token=hf_token
    )
chat_model = ChatHuggingFace(llm =llm)
@tool 
def margin_calculator(revenue:float , operating_cost:float)->str:
    "Calculates the profit margin percentage. ALWAYS use this if you need to find the margin from revenue and costs."
    margin = ((revenue - operating_cost)/revenue)*100
    return f"the precise calculated profit margin is {margin:.2f}%"
tool_box = [margin_calculator]

def supervisor_node(state:SwarmState):
    next_agent = {"next_agent":"analyst"}
    return next_agent


def analyst_node(state: SwarmState):
    user_message = state["messages"][-1]
    #analyst_brain = chat_model.bind_tools(tool_box)
    prompt = f"You are a brilliant hedge fund analyst. Analyze this text: {user_message} If you need to calculate a profit margin, you MUST use the margin_calculator tool."
    response = chat_model.invoke(prompt)
    return {"messages":[response]}

def risk_node(state:SwarmState):
    original_data = state["messages"][0]
    prompt  = f"You are a strict, pessimistic Hedge Fund Risk Manager. Look at this financial data and ONLY point out the macroeconomic dangers, risks, and reasons we should NOT invest: {original_data}"
    response = chat_model.invoke(prompt)
    return {"messages": [f"\nRISK MANAGER REPORT\n{response.content}"]}
tool_node = ToolNode(tool_box)
builder = StateGraph(SwarmState)
builder.add_node("Supervisor", supervisor_node)
builder.add_node("Analyst", analyst_node)
#builder.add_node("tools",tool_node)
builder.add_node("RiskManager",risk_node)

builder.add_edge(START,"Supervisor")
builder.add_edge("Supervisor","Analyst")
"""builder.add_conditional_edges(
   "Analyst",
    tools_condition ,
    {"tools": "tools", "__end__": "RiskManager"}
)"""
builder.add_edge("Analyst","RiskManager")
builder.add_edge("RiskManager",END)
memory = MemorySaver()

marketmind = builder.compile(
    checkpointer=memory , 
    interrupt_before=["RiskManager"]
)

if __name__ == "__main__":
    print("Waking up the MarketMind Swarm...")

    harvester = NewsHarvester()
    target_ticker = "TESLA"
    scraped_data = harvester.fetch_live_news(target_ticker)
    
    if not scraped_data:
        print(f"\nYahoo Finance firewall detected! Using official SEC fallback data for {target_ticker}...\n")
        combined_financial_text = "Tesla, Inc. designs, develops, manufactures, sells and leases high-performance fully electric vehicles and energy generation and storage systems. Our revenue growth is heavily dependent on the global adoption rate of EVs and the expansion of our Supercharger network. We face severe macroeconomic headwinds in the European market due to supply chain constraints and fluctuating raw material costs. However, operating margins improved by 200 basis points driven by software-related profits from Full Self-Driving subscriptions."
    else:
        combined_financial_text = " ".join(scraped_data)
        print(f"\nSuccessfully harvested live data for {target_ticker}. Waking up the Swarm...\n")

    initial_state = {
        "messages": [f"Analyze this company data: {combined_financial_text}"],
        "next_agent": ""
    }
    thread_config = {"configurable": {"thread_id": "trade_execution_3"}}
    
    print("Routing task through the graph...")
    
    marketmind.invoke(initial_state,config = thread_config)
    current_state = marketmind.get_state(thread_config)
    print(current_state.values["messages"][-1])
    print("SECURITY PAUSE: Awaiting Human Authorization")
    user_approval = input("Do you send this to risk manager for final review say yes or no ")
    if user_approval.lower() in ["yes","y"]:
        print("Autorzed proceeding forward")
        final_state = marketmind.invoke(None,config = thread_config)
        print(final_state["messages"][-1])
    else:
        print("/nTrade aborted by Human operator.Shutting down Swarm ")

