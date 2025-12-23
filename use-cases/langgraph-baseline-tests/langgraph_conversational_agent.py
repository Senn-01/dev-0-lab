"""
LangGraph Conversational Agent with Memory and Checkpointing

This implementation demonstrates:
1. Conversation history maintenance across multiple turns
2. Checkpointing for persistence using MemorySaver
3. Thread-based conversation isolation
4. Claude as the LLM
"""

import os
from typing import Annotated, TypedDict, Sequence
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# Define the state schema
class AgentState(TypedDict):
    """
    State schema for our conversational agent.

    The `add_messages` function is a reducer that appends new messages
    to the existing list rather than replacing it.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Initialize the LLM (Claude)
def create_llm():
    """
    Create and configure the Claude LLM.
    Assumes ANTHROPIC_API_KEY is set in environment variables.
    """
    return ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0.7,
        max_tokens=1024
    )


# Define the agent node
def call_model(state: AgentState) -> AgentState:
    """
    Agent node that calls the LLM with the current conversation history.

    Args:
        state: Current agent state containing message history

    Returns:
        Updated state with the model's response appended
    """
    llm = create_llm()
    messages = state["messages"]

    # Call the LLM with the full conversation history
    response = llm.invoke(messages)

    # Return the updated state with the new message
    return {"messages": [response]}


# Build the graph
def create_agent():
    """
    Create the LangGraph conversational agent with checkpointing.

    Returns:
        Compiled graph with memory checkpointing enabled
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)

    # Add the agent node
    workflow.add_node("agent", call_model)

    # Set the entry point
    workflow.set_entry_point("agent")

    # Add an edge from agent back to END
    # This creates a simple one-step conversation flow
    workflow.add_edge("agent", END)

    # Initialize memory checkpointer
    # MemorySaver stores checkpoints in memory (for production, use SqliteSaver or PostgresSaver)
    memory = MemorySaver()

    # Compile the graph with checkpointing
    app = workflow.compile(checkpointer=memory)

    return app


def chat(app, thread_id: str, user_message: str):
    """
    Send a message and get a response, maintaining conversation history.

    Args:
        app: Compiled LangGraph application
        thread_id: Unique identifier for this conversation thread
        user_message: The user's message

    Returns:
        The assistant's response
    """
    # Configure the thread for this conversation
    config = {"configurable": {"thread_id": thread_id}}

    # Create the input state with the user's message
    input_state = {"messages": [HumanMessage(content=user_message)]}

    # Invoke the agent with checkpointing
    # The checkpointer will automatically load previous messages for this thread_id
    # and save the new messages after processing
    output = app.invoke(input_state, config=config)

    # Extract and return the assistant's response
    return output["messages"][-1].content


def get_conversation_history(app, thread_id: str):
    """
    Retrieve the full conversation history for a thread.

    Args:
        app: Compiled LangGraph application
        thread_id: Unique identifier for the conversation thread

    Returns:
        List of all messages in the conversation
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Get the current state for this thread
    state = app.get_state(config)

    # Return the messages if they exist, otherwise empty list
    return state.values.get("messages", []) if state.values else []


def print_conversation(messages: Sequence[BaseMessage]):
    """Pretty print a conversation history."""
    print("\n" + "="*60)
    print("CONVERSATION HISTORY")
    print("="*60)

    for msg in messages:
        if isinstance(msg, HumanMessage):
            print(f"\nUser: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"\nAssistant: {msg.content}")

    print("\n" + "="*60 + "\n")


def main():
    """
    Demonstration of the conversational agent with memory.

    Shows:
    1. Multi-turn conversation within a thread
    2. Conversation persistence via thread_id
    3. Starting a new conversation with a different thread_id
    4. Resuming a previous conversation
    """
    print("Creating LangGraph Conversational Agent with Memory...\n")

    # Create the agent
    app = create_agent()

    # Example 1: Multi-turn conversation in Thread 1
    print("="*60)
    print("EXAMPLE 1: Multi-turn conversation (Thread 1)")
    print("="*60)

    thread1 = "conversation-001"

    print("\nTurn 1:")
    response1 = chat(app, thread1, "Hi! My name is Alice and I love astronomy.")
    print(f"User: Hi! My name is Alice and I love astronomy.")
    print(f"Assistant: {response1}")

    print("\nTurn 2:")
    response2 = chat(app, thread1, "What's my name and what do I love?")
    print(f"User: What's my name and what do I love?")
    print(f"Assistant: {response2}")

    print("\nTurn 3:")
    response3 = chat(app, thread1, "Can you recommend a book related to my interest?")
    print(f"User: Can you recommend a book related to my interest?")
    print(f"Assistant: {response3}")

    # Show full conversation history
    history1 = get_conversation_history(app, thread1)
    print_conversation(history1)

    # Example 2: Different conversation in Thread 2
    print("="*60)
    print("EXAMPLE 2: New conversation (Thread 2)")
    print("="*60)

    thread2 = "conversation-002"

    print("\nTurn 1:")
    response4 = chat(app, thread2, "Hi! I'm Bob and I'm learning to cook.")
    print(f"User: Hi! I'm Bob and I'm learning to cook.")
    print(f"Assistant: {response4}")

    print("\nTurn 2:")
    response5 = chat(app, thread2, "What's my name?")
    print(f"User: What's my name?")
    print(f"Assistant: {response5}")

    # Show that Thread 2 has its own isolated history
    history2 = get_conversation_history(app, thread2)
    print_conversation(history2)

    # Example 3: Resume Thread 1
    print("="*60)
    print("EXAMPLE 3: Resuming Thread 1")
    print("="*60)

    print("\nTurn 4 (continuing from earlier):")
    response6 = chat(app, thread1, "Actually, what was the first thing I told you?")
    print(f"User: Actually, what was the first thing I told you?")
    print(f"Assistant: {response6}")

    # Show updated history for Thread 1
    history1_updated = get_conversation_history(app, thread1)
    print_conversation(history1_updated)

    print("="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nKey takeaways:")
    print("1. Each thread_id maintains its own conversation history")
    print("2. Conversations persist across multiple invocations")
    print("3. The agent remembers context within a thread")
    print("4. Different threads are completely isolated from each other")
    print("5. Checkpointing automatically saves and loads state")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it before running this script:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        exit(1)

    main()
