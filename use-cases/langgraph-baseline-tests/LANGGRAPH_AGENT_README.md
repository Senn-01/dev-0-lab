# LangGraph ReAct Agent Implementation

## Overview

This is a complete implementation of a ReAct-style agent using LangGraph and Claude (Anthropic). The agent can reason about when to use tools versus responding directly.

## Architecture

### Key Components

1. **State Management (`AgentState`)**
   - Uses TypedDict for type safety
   - Maintains conversation history as a sequence of messages
   - Uses `operator.add` annotation for message accumulation

2. **Tools**
   - `web_search`: Simulated web search tool
   - `calculator`: Mathematical expression evaluator
   - Both decorated with `@tool` for LangChain compatibility

3. **Graph Structure**
   - **Agent Node**: Calls Claude to decide next action
   - **Tools Node**: Executes selected tools
   - **Conditional Logic**: Routes based on whether tools are needed

4. **LLM Integration**
   - Uses `ChatAnthropic` with Claude Sonnet 4.5
   - Tools bound using `.bind_tools()` for function calling

## Implementation Choices

### Why LangGraph?

LangGraph provides:
- Explicit control flow visualization
- State persistence and checkpointing capabilities
- Easy debugging of multi-step reasoning
- Native support for cycles (tools → agent → tools)

### ReAct Pattern

The implementation follows the ReAct (Reasoning + Acting) pattern:
1. **Reason**: Claude analyzes the question
2. **Act**: Decides to use tools or respond
3. **Observe**: Processes tool results
4. **Repeat**: Cycles until answer is complete

### State Design

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
```

- Simple, append-only message history
- Type-safe with proper annotations
- Compatible with LangChain message types

### Control Flow

```
Entry → Agent → Should Continue?
                    ↓            ↓
                  Tools        End
                    ↓
                  Agent (loop)
```

The `should_continue` function checks if the last message contains tool calls to determine routing.

## Setup

### Install Dependencies

```bash
# Using uv (recommended)
uv pip install -r langgraph_requirements.txt

# Or using pip
pip install -r langgraph_requirements.txt
```

### Set API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Run Examples

```bash
python langgraph_react_agent.py
```

### Use Programmatically

```python
from langgraph_react_agent import run_agent

# Ask a question
answer = run_agent("What is 150 * 23?")
print(answer)
```

## Example Interactions

### Example 1: Web Search
```
Question: Who created Claude AI?
Agent: [Calling tools: ['web_search']]
Tool Result: Search results for 'Claude AI creator'...
Agent: Claude was created by Anthropic...
```

### Example 2: Calculator
```
Question: What is 142 * 57?
Agent: [Calling tools: ['calculator']]
Tool Result: The result of 142 * 57 is 8094
Agent: The result is 8094.
```

### Example 3: Direct Response
```
Question: What is the capital of France?
Agent: The capital of France is Paris.
```

## Extending the Agent

### Add New Tools

```python
@tool
def my_custom_tool(param: str) -> str:
    """Description of what the tool does."""
    # Implementation
    return result

# Add to tools list
tools = [web_search, calculator, my_custom_tool]
```

### Modify State

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    custom_field: str  # Add your fields
    iteration_count: int
```

### Add Memory/Checkpointing

```python
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(checkpointer=memory)
```

## Production Considerations

1. **Real Web Search**: Replace simulated search with Tavily, SerpAPI, or similar
2. **Safe Calculator**: Use `ast.literal_eval` or a proper math parser
3. **Error Handling**: Add try-catch blocks and graceful degradation
4. **Rate Limiting**: Implement API call throttling
5. **Logging**: Add structured logging for debugging
6. **Streaming**: Use `.astream()` for real-time responses
7. **Caching**: Implement result caching for common queries

## Key Differences from Other Frameworks

### vs. Pure LangChain
- LangGraph gives explicit graph visualization
- Better control over execution flow
- Built-in state persistence

### vs. CrewAI
- More low-level control
- Single-agent focused (can scale to multi-agent)
- Lighter weight

### vs. AutoGPT
- More structured and predictable
- Explicit tool definition
- Better type safety

## Debugging

### Visualize the Graph

```python
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

### Inspect State

```python
result = app.invoke(initial_state)
print(result["messages"])  # See all messages
```

## License

MIT
