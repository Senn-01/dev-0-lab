# LangGraph Conversational Agent Implementation Guide

## Overview

This implementation demonstrates a production-ready conversational agent using LangGraph with full memory and checkpointing capabilities. The agent maintains conversation history across multiple turns and can be resumed using thread IDs.

## Architecture

### Core Components

#### 1. State Management (`AgentState`)

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

- **Purpose**: Defines the shape of data flowing through the graph
- **`messages`**: List of conversation messages (HumanMessage, AIMessage)
- **`add_messages` reducer**: Appends new messages instead of replacing (critical for memory)

**Why this matters**: The `add_messages` annotation is what enables memory. Without it, each invocation would replace the entire message list, losing history.

#### 2. LLM Integration (`create_llm`)

```python
def create_llm():
    return ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0.7,
        max_tokens=1024
    )
```

- **Model**: Claude Sonnet 4.5 (latest as of implementation)
- **Temperature**: 0.7 for balanced creativity/consistency
- **Max tokens**: 1024 (adjust based on needs)

**Design choice**: Creating LLM in a function allows for easy configuration changes and potential dynamic model selection.

#### 3. Agent Node (`call_model`)

```python
def call_model(state: AgentState) -> AgentState:
    llm = create_llm()
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

- **Input**: Current state with full message history
- **Process**: Invokes LLM with all previous messages
- **Output**: Returns new message to be added to state

**Key insight**: The entire conversation history is passed to the LLM on each turn. This is how the model maintains context.

#### 4. Graph Construction (`create_agent`)

```python
def create_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app
```

**Graph structure**:
- Single node: "agent" (the LLM call)
- Linear flow: START → agent → END
- Checkpointer: MemorySaver for persistence

**Why MemorySaver?**
- Stores checkpoints in memory (fast, simple)
- For production: Use `SqliteSaver` or `PostgresSaver` for durability
- Automatically saves state after each invocation
- Automatically loads state before each invocation

#### 5. Conversation Interface (`chat`)

```python
def chat(app, thread_id: str, user_message: str):
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {"messages": [HumanMessage(content=user_message)]}
    output = app.invoke(input_state, config=config)
    return output["messages"][-1].content
```

**Critical elements**:
- **`thread_id`**: Isolates conversations (different IDs = different histories)
- **`config`**: Passed to checkpointer to identify which conversation to load/save
- **Input state**: Only includes the new message (history loaded automatically)
- **Return**: Extracts just the assistant's response

## Memory & Checkpointing Explained

### How Checkpointing Works

1. **First message in a thread**:
   - Checkpointer finds no existing state for this thread_id
   - Creates new state with just the user's message
   - Graph executes, adds AI response
   - Checkpointer saves complete state

2. **Subsequent messages**:
   - Checkpointer loads saved state for thread_id
   - Merges new user message using `add_messages` reducer
   - Graph executes with full history
   - Checkpointer saves updated state

3. **Resuming conversations**:
   - Same thread_id retrieves the same checkpoint
   - Full history is available immediately
   - No explicit "load" required - automatic

### Thread Isolation

```python
# Thread 1
chat(app, "thread-1", "My name is Alice")
chat(app, "thread-1", "What's my name?")  # Will say Alice

# Thread 2
chat(app, "thread-2", "My name is Bob")
chat(app, "thread-2", "What's my name?")  # Will say Bob

# Back to Thread 1
chat(app, "thread-1", "And what about now?")  # Still knows Alice
```

Each thread_id maintains completely separate state. This enables:
- Multiple concurrent users
- Different conversation topics
- A/B testing different approaches
- Conversation branching

## Implementation Choices Explained

### 1. Why TypedDict for State?

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

**Alternatives considered**:
- Pydantic models: More validation but slower
- Plain dict: No type safety
- dataclass: Doesn't support annotations well

**Chosen because**:
- Native Python (Python 3.8+)
- Supports `Annotated` for reducers
- Fast and lightweight
- Type hints for IDE support

### 2. Why `add_messages` Reducer?

Without the reducer:
```python
# Each turn would be:
state = {"messages": [new_message]}  # Previous messages lost!
```

With the reducer:
```python
# Each turn appends:
state = {"messages": [...previous, new_message]}  # History preserved
```

The `add_messages` reducer is LangGraph's way of specifying "append, don't replace."

### 3. Why Simple Linear Graph?

```
START → agent → END
```

**Could have**:
- Loops (agent → agent for multi-step reasoning)
- Conditional edges (routing to different nodes)
- Multiple nodes (retrieval, tools, etc.)

**Chose simple because**:
- Demonstrates core memory concept clearly
- Easy to understand and extend
- Sufficient for most conversational use cases
- Can add complexity as needed

**Extension example**:
```python
# Add tool calling
workflow.add_node("agent", call_model)
workflow.add_node("tools", execute_tools)
workflow.add_conditional_edges(
    "agent",
    should_use_tools,
    {True: "tools", False: END}
)
workflow.add_edge("tools", "agent")
```

### 4. Why MemorySaver vs Other Checkpointers?

| Checkpointer | Use Case | Pros | Cons |
|-------------|----------|------|------|
| MemorySaver | Development, testing | Fast, simple | Lost on restart |
| SqliteSaver | Single-server production | Persistent, local | Not distributed |
| PostgresSaver | Multi-server production | Distributed, scalable | Requires DB setup |

**Recommendation**:
- Development: MemorySaver
- Production (single instance): SqliteSaver
- Production (distributed): PostgresSaver

**Migration path**:
```python
# Development
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# Production
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("checkpoints.db")

# Distributed
from langgraph.checkpoint.postgres import PostgresSaver
memory = PostgresSaver.from_conn_string("postgresql://...")
```

### 5. Why Return Only Last Message?

```python
return output["messages"][-1].content
```

**Alternatives**:
- Return full output state
- Return all messages
- Return structured response

**Chosen because**:
- Matches typical chatbot UX (user sees latest response)
- Full history available via `get_conversation_history()`
- Cleaner API for simple use cases

## Usage Patterns

### Basic Conversation

```python
app = create_agent()
thread_id = "user-123"

# Turn 1
response = chat(app, thread_id, "Hello!")
print(response)

# Turn 2 - remembers context
response = chat(app, thread_id, "What did I just say?")
print(response)  # Will reference "Hello!"
```

### Multiple Users

```python
app = create_agent()

# User 1
chat(app, "user-1", "My favorite food is pizza")

# User 2
chat(app, "user-2", "My favorite food is sushi")

# User 1 continues - isolated context
chat(app, "user-1", "What's my favorite food?")  # "pizza"
```

### Retrieving History

```python
app = create_agent()
thread_id = "session-456"

# Have conversation
chat(app, thread_id, "Tell me about Python")
chat(app, thread_id, "What about JavaScript?")

# Get full history
history = get_conversation_history(app, thread_id)
for msg in history:
    print(f"{msg.__class__.__name__}: {msg.content}")
```

### Production Considerations

```python
# Add error handling
def chat_with_retry(app, thread_id, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chat(app, thread_id, message)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# Add timeout
import signal
def chat_with_timeout(app, thread_id, message, timeout=30):
    signal.alarm(timeout)
    try:
        return chat(app, thread_id, message)
    finally:
        signal.alarm(0)

# Add logging
import logging
def chat_logged(app, thread_id, message):
    logging.info(f"Chat started - Thread: {thread_id}")
    response = chat(app, thread_id, message)
    logging.info(f"Chat completed - Response length: {len(response)}")
    return response
```

## Testing

Run the test suite:

```bash
python test_langgraph_agent.py
```

Tests verify:
1. Memory persistence across turns
2. Thread isolation
3. History retrieval

## Extending the Implementation

### Adding Tools/Function Calling

```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Bind tools to LLM
llm = create_llm().bind_tools([get_weather])
```

### Adding Retrieval (RAG)

```python
def retrieval_node(state: AgentState):
    query = state["messages"][-1].content
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs])
    # Add context to message or state
    return state
```

### Adding Conversation Summary

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    summary: str  # Add summary field

def summarize_node(state: AgentState):
    if len(state["messages"]) > 10:
        # Summarize conversation
        summary = llm.invoke([
            SystemMessage("Summarize this conversation"),
            *state["messages"]
        ])
        # Trim messages, keep summary
        return {
            "messages": state["messages"][-5:],
            "summary": summary.content
        }
    return state
```

## Common Pitfalls

### 1. Forgetting the Reducer

```python
# WRONG - Will lose history
messages: Sequence[BaseMessage]

# RIGHT - Preserves history
messages: Annotated[Sequence[BaseMessage], add_messages]
```

### 2. Not Passing Config

```python
# WRONG - Creates new thread each time
app.invoke(input_state)

# RIGHT - Maintains thread
app.invoke(input_state, config={"configurable": {"thread_id": id}})
```

### 3. Replacing Instead of Appending

```python
# WRONG - Loses previous messages
return {"messages": [response]}  # Only if using add_messages reducer

# If not using reducer:
return {"messages": state["messages"] + [response]}
```

### 4. Inconsistent Thread IDs

```python
# WRONG - Different IDs = Different conversations
chat(app, "thread-1", "Hello")
chat(app, "thread-2", "What did I say?")  # Won't remember

# RIGHT - Same ID = Same conversation
chat(app, "thread-1", "Hello")
chat(app, "thread-1", "What did I say?")  # Remembers
```

## Performance Considerations

### Message List Growth

As conversations grow, passing full history becomes expensive:

```python
# Solution 1: Sliding window
def trim_messages(messages, keep_last=20):
    return messages[-keep_last:]

# Solution 2: Summarization
def summarize_old_messages(messages, threshold=50):
    if len(messages) > threshold:
        # Summarize older messages
        # Keep recent messages as-is
        pass
```

### Checkpointer Performance

| Checkpointer | Read Speed | Write Speed | Concurrent Users |
|-------------|-----------|-------------|------------------|
| MemorySaver | Fastest | Fastest | Low |
| SqliteSaver | Fast | Medium | Medium |
| PostgresSaver | Medium | Medium | High |

### Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_response(message_hash):
    # Cache responses for identical messages
    pass
```

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect State at Each Step

```python
# Get state for a thread
config = {"configurable": {"thread_id": "debug-001"}}
state = app.get_state(config)
print(state.values)
print(state.next)  # Next nodes to execute
```

### Print Message Flow

```python
def chat_debug(app, thread_id, message):
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {"messages": [HumanMessage(content=message)]}

    print(f"Input: {message}")
    print(f"Thread: {thread_id}")

    output = app.invoke(input_state, config=config)

    print(f"Messages in state: {len(output['messages'])}")
    for msg in output["messages"]:
        print(f"  - {msg.__class__.__name__}: {msg.content[:50]}...")

    return output["messages"][-1].content
```

## Conclusion

This implementation provides a solid foundation for conversational AI applications with:

- ✓ Full memory persistence
- ✓ Thread-based isolation
- ✓ Production-ready architecture
- ✓ Easy to extend
- ✓ Type-safe
- ✓ Well-tested

The key insight is that LangGraph's checkpointing + state reducers handle all the complexity of memory management, allowing you to focus on the conversation logic itself.
