"""
Simple ReAct Agent using LangGraph

This implementation creates a ReAct-style agent that:
1. Takes user questions as input
2. Has access to web search and calculator tools
3. Uses Claude (Anthropic) as the LLM
4. Decides when to use tools vs respond directly
"""

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os


# Define tools
@tool
def web_search(query: str) -> str:
    """Search the web for information about a query.

    Args:
        query: The search query string

    Returns:
        Search results as a string
    """
    # Simulated web search - in production, you'd use a real API like Tavily, SerpAPI, etc.
    return f"Search results for '{query}': [Simulated] Claude is an AI assistant created by Anthropic. It uses constitutional AI methods for safer, more helpful responses."


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")

    Returns:
        The result of the calculation as a string
    """
    try:
        # Safe evaluation of mathematical expressions
        # In production, use a proper math parser library for safety
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


# Define the agent state
class AgentState(TypedDict):
    """State of the agent, tracking the conversation history."""
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Initialize the LLM with tools
tools = [web_search, calculator]
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
llm_with_tools = llm.bind_tools(tools)


# Define agent logic
def should_continue(state: AgentState) -> str:
    """Determine if the agent should continue or end.

    Args:
        state: Current agent state

    Returns:
        "tools" if the agent wants to use tools, "end" otherwise
    """
    messages = state["messages"]
    last_message = messages[-1]

    # If there are no tool calls, we're done
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "tools"


def call_model(state: AgentState) -> dict:
    """Call the LLM to decide next action.

    Args:
        state: Current agent state

    Returns:
        Dictionary with updated messages
    """
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.set_entry_point("agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

# Add edge from tools back to agent
workflow.add_edge("tools", "agent")

# Compile the graph
app = workflow.compile()


def run_agent(question: str) -> str:
    """Run the agent with a user question.

    Args:
        question: The user's question

    Returns:
        The agent's final response
    """
    initial_state = {
        "messages": [HumanMessage(content=question)]
    }

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}\n")

    # Run the agent
    result = app.invoke(initial_state)

    # Extract and display the conversation
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"Human: {msg.content}\n")
        elif isinstance(msg, AIMessage):
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print(f"Agent: [Calling tools: {[tc['name'] for tc in msg.tool_calls]}]")
            else:
                print(f"Agent: {msg.content}\n")
        elif isinstance(msg, ToolMessage):
            print(f"Tool Result: {msg.content}\n")

    # Return the final response
    final_message = result["messages"][-1]
    return final_message.content if hasattr(final_message, "content") else str(final_message)


if __name__ == "__main__":
    # Example 1: Question requiring web search
    print("\n" + "="*60)
    print("EXAMPLE 1: Web Search")
    print("="*60)
    answer1 = run_agent("Who created Claude AI?")

    # Example 2: Question requiring calculator
    print("\n" + "="*60)
    print("EXAMPLE 2: Calculator")
    print("="*60)
    answer2 = run_agent("What is 142 * 57?")

    # Example 3: Question requiring both tools
    print("\n" + "="*60)
    print("EXAMPLE 3: Multiple Tools")
    print("="*60)
    answer3 = run_agent("Search for information about Claude AI and calculate 25 + 75")

    # Example 4: Direct response (no tools needed)
    print("\n" + "="*60)
    print("EXAMPLE 4: Direct Response")
    print("="*60)
    answer4 = run_agent("What is the capital of France?")

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
