# Quick Start Guide - Customer Support Workflow

## 5-Minute Setup

### 1. Install Dependencies
```bash
# Create virtual environment
uv venv

# Install required packages
uv pip install langgraph anthropic python-dotenv
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run Tests (No API Key Required)
```bash
source .venv/bin/activate
python test_customer_support.py
```

Output shows:
- Graph structure (nodes and edges)
- State flow validation
- Routing logic tests
- Example tickets
- Design benefits

### 4. View Workflow Diagram
```bash
python workflow_diagram.py
```

Shows visual representation of the workflow.

### 5. Run Full Workflow (API Key Required)
```bash
python customer_support_workflow.py
```

Processes 3 example tickets:
1. Billing: Duplicate charge
2. Technical: App crash
3. General: Business hours inquiry

## Code Structure

```
customer_support_workflow.py          # Main implementation (400 lines)
├── TicketState (TypedDict)          # State definition
├── classify_ticket()                # Node 1: Classification
├── route_ticket()                   # Conditional routing
├── handle_billing()                 # Node 2a: Billing handler
├── handle_technical()               # Node 2b: Technical handler
├── handle_general()                 # Node 2c: General handler
├── format_response()                # Node 3: Formatting
├── build_workflow()                 # Graph construction
└── process_ticket()                 # Main entry point
```

## Usage Examples

### Basic Usage
```python
from customer_support_workflow import process_ticket

result = process_ticket(
    ticket_id="TKT-123",
    ticket_content="I can't log into my account"
)

print(result["formatted_response"])
print(f"Category: {result['classification']}")
```

### Custom Integration
```python
from customer_support_workflow import build_workflow

workflow = build_workflow()
app = workflow.compile()

state = {
    "ticket_id": "CUSTOM-001",
    "ticket_content": "Your content here",
    "classification": "",
    "handler_response": "",
    "formatted_response": ""
}

result = app.invoke(state)
```

### Streaming Results
```python
for step in app.stream(state):
    print(f"Current node: {step}")
```

## Graph Structure

```
START → classify → route → [billing|technical|general] → format → END
```

**Nodes:**
- `classify`: Uses Claude to categorize ticket
- `route`: Conditional branching logic
- `billing/technical/general`: Specialized handlers
- `format`: Wraps response in template

**State Flow:**
1. Initial: All fields empty except ticket_id and ticket_content
2. After classify: classification field set
3. After handler: handler_response field set
4. After format: formatted_response field set

## Adding a New Category

```python
# 1. Update classify prompt to include new category

# 2. Create handler
def handle_sales(state: TicketState) -> TicketState:
    # Your logic here
    return state

# 3. Add to graph
workflow.add_node("sales", handle_sales)

# 4. Update routing
workflow.add_conditional_edges(
    "classify",
    route_ticket,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general",
        "sales": "sales"  # New
    }
)

# 5. Connect to format
workflow.add_edge("sales", "format")
```

## Customizing Prompts

Edit the handler functions:

```python
def handle_billing(state: TicketState) -> TicketState:
    client = get_anthropic_client()

    # Customize this prompt
    prompt = f"""You are a billing support specialist...
    {state['ticket_content']}
    Your custom instructions here..."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    state["handler_response"] = message.content[0].text.strip()
    return state
```

## Performance Tips

1. **Cache Classifications**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=1000)
   def cached_classify(content: str) -> str:
       return classify_ticket_logic(content)
   ```

2. **Use Streaming**
   ```python
   message = client.messages.create(
       model="claude-sonnet-4-5-20250929",
       max_tokens=500,
       messages=[{"role": "user", "content": prompt}],
       stream=True
   )
   ```

3. **Batch Processing**
   ```python
   import asyncio

   async def process_tickets_batch(tickets):
       tasks = [process_ticket_async(t) for t in tickets]
       return await asyncio.gather(*tasks)
   ```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key"
# Or create .env file
```

### "No module named 'langgraph'"
```bash
uv pip install langgraph anthropic
```

### Classification returns wrong category
- Check the classification prompt in `classify_ticket()`
- Ensure prompt is clear and includes examples
- Add fallback logic for edge cases

### Handler produces poor responses
- Improve the handler-specific prompt
- Add more context or examples
- Increase max_tokens if responses are cut off

## Testing

### Test Graph Structure
```bash
python test_customer_support.py
```

### Test with Real API
```bash
python customer_support_workflow.py
```

### Test Custom Ticket
```python
from customer_support_workflow import process_ticket

result = process_ticket(
    ticket_id="TEST-001",
    ticket_content="Your test content here"
)
```

## Key Files

- **customer_support_workflow.py** - Main implementation
- **test_customer_support.py** - Test suite (no API calls)
- **workflow_diagram.py** - Visual documentation
- **CUSTOMER_SUPPORT_README.md** - Full documentation
- **IMPLEMENTATION_SUMMARY.md** - Technical deep-dive
- **QUICK_START.md** - This file

## Next Steps

1. Read CUSTOMER_SUPPORT_README.md for comprehensive docs
2. Read IMPLEMENTATION_SUMMARY.md for technical details
3. Run tests to validate installation
4. Customize prompts for your use case
5. Add error handling for production
6. Implement monitoring and logging
7. Add rate limiting and caching

## Support

For questions about:
- **LangGraph** - See https://langchain-ai.github.io/langgraph/
- **Anthropic Claude** - See https://docs.anthropic.com/
- **This Implementation** - See CUSTOMER_SUPPORT_README.md

## License

MIT License - Free to use and modify for your projects.
