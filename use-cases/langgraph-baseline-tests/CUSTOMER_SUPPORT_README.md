# Customer Support Ticket Workflow - LangGraph Implementation

A comprehensive multi-step workflow built with LangGraph that intelligently processes customer support tickets using Claude AI for classification, routing, and response generation.

## Overview

This workflow demonstrates a real-world customer support automation system that:
1. **Classifies** incoming tickets into categories (billing, technical, general)
2. **Routes** tickets to specialized handlers based on classification
3. **Generates** appropriate responses using domain-specific prompts
4. **Formats** the final response in a professional email template

## Architecture

### State Management

The workflow uses a strongly-typed state object (`TicketState`) that flows through all nodes:

```python
class TicketState(TypedDict):
    ticket_id: str           # Unique ticket identifier
    ticket_content: str      # Customer's message
    classification: str      # Determined category (billing/technical/general)
    handler_response: str    # Response from specialized handler
    formatted_response: str  # Final formatted output
```

### Graph Structure

```
START
  │
  ▼
┌─────────────┐
│  classify   │  ← Classifies ticket using Claude
└─────────────┘
  │
  ▼
┌─────────────┐
│    route    │  ← Conditional routing logic
└─────────────┘
  │  │  │
  │  │  └──────┐
  │  └────┐    │
  ▼       ▼    ▼
┌────┐ ┌────┐ ┌────┐
│bill│ │tech│ │gen │  ← Specialized handlers
└────┘ └────┘ └────┘
  │       │    │
  └───┬───┘    │
      │        │
      ▼        ▼
  ┌─────────────┐
  │   format    │  ← Final formatting
  └─────────────┘
      │
      ▼
     END
```

### Workflow Nodes

1. **classify_ticket** (Node 1)
   - Uses Claude to analyze ticket content
   - Determines category: billing, technical, or general
   - Prompt engineered for accurate classification
   - Includes fallback to "general" for edge cases

2. **route_ticket** (Conditional Edge)
   - Examines the classification from state
   - Returns routing decision as Literal type
   - LangGraph uses this to select the next node

3. **handle_billing** (Node 2a)
   - Specialized prompt for billing issues
   - Focuses on: payments, refunds, subscriptions
   - Acknowledges concern and offers solutions
   - Mentions escalation path if needed

4. **handle_technical** (Node 2b)
   - Specialized prompt for technical problems
   - Focuses on: bugs, errors, troubleshooting
   - Provides diagnostic steps
   - Requests additional information (logs, screenshots)

5. **handle_general** (Node 2c)
   - Handles inquiries, questions, feedback
   - Friendly, informative tone
   - Offers additional resources
   - Thanks customer for reaching out

6. **format_response** (Node 3)
   - Creates professional email template
   - Includes ticket ID and category
   - Wraps handler response in branded format
   - Adds signature and footer

## Implementation Choices

### Why LangGraph?

1. **State Management**: LangGraph's typed state objects provide type safety and clear data flow
2. **Conditional Routing**: Native support for dynamic branching based on state
3. **Composability**: Easy to add new handlers or modify the workflow
4. **Debugging**: Built-in visualization and state inspection capabilities

### Why Claude?

1. **Context Understanding**: Excellent at nuanced classification tasks
2. **Response Quality**: Generates professional, empathetic customer support responses
3. **Consistency**: Reliable output format across multiple calls
4. **Speed**: Fast enough for real-time customer support scenarios

### Design Patterns

1. **Separation of Concerns**
   - Each handler has a single responsibility
   - Classification logic is isolated from response generation
   - Formatting is decoupled from content creation

2. **Type Safety**
   - TypedDict for state ensures compile-time checking
   - Literal types for routing provide exhaustive checking
   - Clear function signatures prevent errors

3. **Extensibility**
   - Easy to add new ticket categories
   - Handler prompts can be customized independently
   - State can be extended without breaking existing nodes

4. **Error Handling**
   - Fallback classification if Claude returns unexpected value
   - Environment variable validation
   - Clear error messages

## Setup

### 1. Install Dependencies

Using UV (recommended):
```bash
uv pip install -r customer_support_requirements.txt
```

Or using standard pip:
```bash
pip install langgraph anthropic python-dotenv
```

### 2. Set Environment Variables

Create a `.env` file or export:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run the Workflow

```bash
python customer_support_workflow.py
```

## Usage

### Basic Usage

```python
from customer_support_workflow import process_ticket

# Process a single ticket
result = process_ticket(
    ticket_id="TKT-123",
    ticket_content="I can't log into my account after resetting my password"
)

# Access the formatted response
print(result["formatted_response"])

# Check the classification
print(f"Classified as: {result['classification']}")
```

### Custom Integration

```python
from customer_support_workflow import build_workflow

# Build the workflow
workflow = build_workflow()
app = workflow.compile()

# Create custom initial state
initial_state = {
    "ticket_id": "CUSTOM-001",
    "ticket_content": "Your ticket content here",
    "classification": "",
    "handler_response": "",
    "formatted_response": ""
}

# Run with custom state
final_state = app.invoke(initial_state)
```

### Streaming Execution

```python
# Stream intermediate results
for step in app.stream(initial_state):
    print(f"Node: {step}")
    print(f"State: {step}")
```

## Testing

The script includes three test cases demonstrating each ticket type:

1. **Billing Test**: Duplicate charge scenario
2. **Technical Test**: App crash with error code
3. **General Test**: Business hours and demo request

Run the tests:
```bash
python customer_support_workflow.py
```

## Customization

### Adding a New Ticket Category

1. Update the classification prompt in `classify_ticket()`
2. Create a new handler function (e.g., `handle_sales()`)
3. Add the node to the graph: `workflow.add_node("sales", handle_sales)`
4. Update routing: Add "sales" to the routing dictionary
5. Connect to format: `workflow.add_edge("sales", "format")`

### Modifying Handler Prompts

Each handler has a prompt template. Customize them to match your:
- Brand voice and tone
- Company policies
- Available resources
- Escalation procedures

### Enhancing State

Add new fields to `TicketState`:
```python
class TicketState(TypedDict):
    # Existing fields...
    customer_id: str
    priority: str
    sentiment: str
    estimated_resolution_time: str
```

## Advanced Features

### 1. Persistence

Add checkpointing for long-running workflows:
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

### 2. Human-in-the-Loop

Add approval nodes before sending responses:
```python
def human_approval(state: TicketState) -> TicketState:
    print(f"Response: {state['handler_response']}")
    approval = input("Approve? (y/n): ")
    state["approved"] = approval == "y"
    return state

workflow.add_node("approval", human_approval)
```

### 3. Multi-Agent Collaboration

Add specialist agents for complex tickets:
```python
def escalate_complex(state: TicketState) -> TicketState:
    # Call senior support agent or specialized system
    pass
```

### 4. Analytics and Logging

Track metrics for optimization:
```python
import time

def classify_ticket(state: TicketState) -> TicketState:
    start_time = time.time()
    # ... existing logic ...
    duration = time.time() - start_time
    log_metric("classification_time", duration)
    return state
```

## Production Considerations

### 1. Rate Limiting

Implement rate limiting for API calls:
```python
from anthropic import RateLimitError
import time

def call_claude_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(...)
        except RateLimitError:
            time.sleep(2 ** attempt)
    raise
```

### 2. Caching

Cache common classifications:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_classify(ticket_content: str) -> str:
    # Classification logic
    pass
```

### 3. Monitoring

Add observability:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_ticket(state: TicketState) -> TicketState:
    logger.info(f"Classifying ticket {state['ticket_id']}")
    # ... rest of function
```

### 4. Error Recovery

Implement graceful error handling:
```python
def safe_classify(state: TicketState) -> TicketState:
    try:
        return classify_ticket(state)
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        state["classification"] = "general"  # Safe default
        return state
```

## Performance

Expected performance with Claude Sonnet 4.5:
- Classification: ~1-2 seconds
- Handler response: ~2-3 seconds
- Total workflow: ~3-5 seconds per ticket

Optimization tips:
- Use streaming for real-time updates
- Implement caching for repeated patterns
- Use async execution for batch processing
- Consider fine-tuning for high-volume scenarios

## Troubleshooting

### API Key Issues
```
ValueError: ANTHROPIC_API_KEY environment variable not set
```
**Solution**: Set the environment variable or create a `.env` file

### Import Errors
```
ModuleNotFoundError: No module named 'langgraph'
```
**Solution**: Install dependencies using the requirements file

### Routing Failures
If tickets aren't routing correctly, check:
1. Classification output format (should be exactly: "billing", "technical", or "general")
2. Routing function return type (must match edge keys)
3. Graph edge connections (all handlers must connect to format)

## License

MIT License - feel free to use and modify for your projects.

## Contributing

Contributions welcome! Areas for improvement:
- Additional ticket categories
- Multi-language support
- Sentiment analysis integration
- Automated testing suite
- Performance benchmarks

## Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [Anthropic Claude](https://www.anthropic.com) - AI reasoning and generation
- [Python TypedDict](https://docs.python.org/3/library/typing.html) - Type safety
