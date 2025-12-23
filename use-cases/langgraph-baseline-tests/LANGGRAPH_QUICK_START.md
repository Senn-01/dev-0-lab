# LangGraph Conversational Agent - Quick Start

## Installation

```bash
# Using uv (recommended)
uv pip install -r langgraph_requirements.txt

# Or using pip
pip install langgraph langchain-anthropic langchain-core
```

## Set Up API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Run the Demo

```bash
python langgraph_conversational_agent.py
```

This will show:
1. A multi-turn conversation in Thread 1
2. A separate conversation in Thread 2
3. Resuming Thread 1 (demonstrates persistence)

## Run Tests

```bash
python test_langgraph_agent.py
```

Tests verify:
- Memory persistence across turns
- Thread isolation
- History retrieval

## Basic Usage

```python
from langgraph_conversational_agent import create_agent, chat

# Create the agent (once)
app = create_agent()

# Start a conversation
thread_id = "user-123"

# Turn 1
response = chat(app, thread_id, "Hello! My name is Alice.")
print(response)

# Turn 2 - agent remembers context
response = chat(app, thread_id, "What's my name?")
print(response)  # Will say "Alice"

# Different thread = different conversation
other_thread = "user-456"
response = chat(app, other_thread, "What's my name?")
print(response)  # Won't know - different conversation
```

## Key Concepts

### Thread ID
- Unique identifier for each conversation
- Same thread_id = same conversation history
- Different thread_id = isolated conversation

### Checkpointing
- Automatically saves state after each turn
- Automatically loads state before each turn
- No manual save/load required

### Message History
- Full conversation history maintained per thread
- Passed to LLM on each turn for context
- Grows unbounded (implement trimming for production)

## Common Patterns

### Single User, Multiple Topics

```python
app = create_agent()

# Topic 1: Cooking
chat(app, "cooking-session", "How do I make pasta?")
chat(app, "cooking-session", "What about the sauce?")

# Topic 2: Gardening
chat(app, "garden-session", "When should I plant tomatoes?")
chat(app, "garden-session", "How often to water?")

# Back to cooking - remembers context
chat(app, "cooking-session", "How long to boil the pasta?")
```

### Multiple Users

```python
app = create_agent()

# User 1
chat(app, "user-alice", "My favorite color is blue")

# User 2
chat(app, "user-bob", "My favorite color is red")

# Each user has isolated context
chat(app, "user-alice", "What's my favorite color?")  # "blue"
chat(app, "user-bob", "What's my favorite color?")    # "red"
```

### Retrieving History

```python
from langgraph_conversational_agent import get_conversation_history

app = create_agent()
thread_id = "my-session"

# Have a conversation
chat(app, thread_id, "Hello")
chat(app, thread_id, "How are you?")

# Get full history
history = get_conversation_history(app, thread_id)

# Print all messages
for msg in history:
    if isinstance(msg, HumanMessage):
        print(f"User: {msg.content}")
    elif isinstance(msg, AIMessage):
        print(f"Assistant: {msg.content}")
```

## Troubleshooting

### "Agent doesn't remember previous messages"

**Check:**
1. Are you using the same `thread_id` for both calls?
2. Is the checkpointer properly compiled into the graph?

```python
# WRONG - Different thread IDs
chat(app, "thread-1", "My name is Alice")
chat(app, "thread-2", "What's my name?")  # Won't remember

# RIGHT - Same thread ID
chat(app, "thread-1", "My name is Alice")
chat(app, "thread-1", "What's my name?")  # Will remember
```

### "API Key Error"

**Solution:**
```bash
# Make sure environment variable is set
export ANTHROPIC_API_KEY='your-key'

# Verify it's set
echo $ANTHROPIC_API_KEY

# Run Python script
python langgraph_conversational_agent.py
```

### "Import Error"

**Solution:**
```bash
# Install dependencies
uv pip install -r langgraph_requirements.txt

# Or
pip install langgraph langchain-anthropic langchain-core
```

## Next Steps

1. **Read the implementation**: `langgraph_conversational_agent.py`
   - Well-commented code explaining each component

2. **Read the guide**: `LANGGRAPH_IMPLEMENTATION_GUIDE.md`
   - Deep dive into architecture decisions
   - Extension patterns
   - Production considerations

3. **Extend the agent**:
   - Add tools/function calling
   - Implement retrieval (RAG)
   - Add conversation summarization
   - Implement message trimming

## Files Overview

| File | Purpose |
|------|---------|
| `langgraph_conversational_agent.py` | Main implementation |
| `test_langgraph_agent.py` | Test suite |
| `LANGGRAPH_IMPLEMENTATION_GUIDE.md` | Comprehensive guide |
| `LANGGRAPH_QUICK_START.md` | This file - quick reference |
| `langgraph_requirements.txt` | Dependencies |

## Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Anthropic API**: https://docs.anthropic.com/
- **LangChain Docs**: https://python.langchain.com/

## Support

If you encounter issues:
1. Check that API key is set correctly
2. Verify dependencies are installed
3. Run test suite to isolate the problem
4. Review implementation guide for architecture details
