"""
Workflow Diagram Generator

Creates a visual representation of the customer support workflow
"""


def print_workflow_diagram():
    """Print an ASCII diagram of the workflow"""

    diagram = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                  CUSTOMER SUPPORT TICKET WORKFLOW                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

                              ┌─────────────┐
                              │   START     │
                              └──────┬──────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │                                │
                    │    NODE 1: CLASSIFY TICKET     │
                    │                                │
                    │  • Analyzes ticket content     │
                    │  • Uses Claude AI              │
                    │  • Returns: billing/           │
                    │    technical/general           │
                    │                                │
                    └────────────┬───────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────────┐
                    │                                │
                    │  CONDITIONAL ROUTING LOGIC     │
                    │                                │
                    │  • Reads 'classification'      │
                    │  • Returns route decision      │
                    │  • Type: Literal[str]          │
                    │                                │
                    └────────────┬───────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
         ┌──────────▼──┐    ┌───▼────────┐  ┌▼──────────┐
         │             │    │            │  │           │
         │   NODE 2a   │    │  NODE 2b   │  │ NODE 2c   │
         │             │    │            │  │           │
         │   BILLING   │    │ TECHNICAL  │  │  GENERAL  │
         │   HANDLER   │    │  HANDLER   │  │  HANDLER  │
         │             │    │            │  │           │
         │  • Refunds  │    │  • Bugs    │  │ • Info    │
         │  • Charges  │    │  • Errors  │  │ • Hours   │
         │  • Invoices │    │  • Logs    │  │ • Demos   │
         │             │    │            │  │           │
         └──────┬──────┘    └──────┬─────┘  └───┬───────┘
                │                  │            │
                └──────────┬───────┴────────────┘
                           │
                           ▼
                ┌──────────────────────────┐
                │                          │
                │   NODE 3: FORMAT         │
                │                          │
                │  • Wraps response        │
                │  • Adds ticket ID        │
                │  • Professional template │
                │  • Signature & footer    │
                │                          │
                └──────────┬───────────────┘
                           │
                           ▼
                      ┌─────────┐
                      │   END   │
                      └─────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                          STATE TRANSFORMATIONS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. INITIAL STATE
   {
     ticket_id: "TKT-001"
     ticket_content: "I was charged twice..."
     classification: ""                         ← Empty
     handler_response: ""                       ← Empty
     formatted_response: ""                     ← Empty
   }

2. AFTER CLASSIFY NODE
   {
     ticket_id: "TKT-001"
     ticket_content: "I was charged twice..."
     classification: "billing"                  ← Set by classify
     handler_response: ""
     formatted_response: ""
   }

3. AFTER HANDLER NODE (billing)
   {
     ticket_id: "TKT-001"
     ticket_content: "I was charged twice..."
     classification: "billing"
     handler_response: "Thank you for..."       ← Set by handler
     formatted_response: ""
   }

4. FINAL STATE (after format)
   {
     ticket_id: "TKT-001"
     ticket_content: "I was charged twice..."
     classification: "billing"
     handler_response: "Thank you for..."
     formatted_response: "━━━━━━..."           ← Set by format
   }


╔══════════════════════════════════════════════════════════════════════════════╗
║                            DECISION POINTS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

ROUTING DECISION (after classify node):

  if classification == "billing":
      → Go to billing handler

  elif classification == "technical":
      → Go to technical handler

  elif classification == "general":
      → Go to general handler

  else:
      → Default to general handler


╔══════════════════════════════════════════════════════════════════════════════╗
║                         EXECUTION EXAMPLE                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Input Ticket:
  ID: TKT-123
  Content: "App crashes when uploading large files"

Execution Trace:
  [1] START
      → Initialize state with ticket data

  [2] CLASSIFY NODE
      → Call Claude: "Analyze and classify this ticket..."
      → Claude Response: "technical"
      → State updated: classification = "technical"
      → Duration: ~1.5s

  [3] ROUTING LOGIC
      → Read state.classification = "technical"
      → Decision: Route to technical handler
      → Duration: <1ms

  [4] TECHNICAL HANDLER NODE
      → Call Claude: "You are a technical support specialist..."
      → Claude Response: "Thank you for reporting... try these steps..."
      → State updated: handler_response = "Thank you for..."
      → Duration: ~2.5s

  [5] FORMAT NODE
      → Wrap response in email template
      → Add ticket ID and category
      → State updated: formatted_response = "━━━━..."
      → Duration: <1ms

  [6] END
      → Return final state
      → Total Duration: ~4s

Output:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CUSTOMER SUPPORT RESPONSE
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Ticket ID: TKT-123
  Category: TECHNICAL

  Dear Valued Customer,

  Thank you for reporting this issue. We understand how
  frustrating it can be when the app crashes during file
  uploads. Based on your description, here are some
  troubleshooting steps...

  Best regards,
  Customer Support Team
  Support Ticket: TKT-123

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


╔══════════════════════════════════════════════════════════════════════════════╗
║                           KEY FEATURES                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

✓ TYPE SAFETY
  • TypedDict for state ensures correctness
  • Literal types for routing prevent errors
  • Compile-time checking with mypy

✓ CONDITIONAL BRANCHING
  • Dynamic routing based on classification
  • Each category gets specialized handling
  • Easy to add new categories

✓ STATE MANAGEMENT
  • Immutable state updates
  • Clear data flow through nodes
  • All transformations tracked

✓ COMPOSABILITY
  • Nodes are independent functions
  • Easy to test in isolation
  • Can be reused in other workflows

✓ OBSERVABILITY
  • Console logging at each step
  • State inspection capabilities
  • Graph visualization support

✓ EXTENSIBILITY
  • Add nodes without breaking existing flow
  • Extend state with new fields
  • Customize prompts independently


╔══════════════════════════════════════════════════════════════════════════════╗
║                        PERFORMANCE PROFILE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Node               | Avg Time  | API Calls | Bottleneck?
-------------------|-----------|-----------|-------------
classify           | ~1.5s     | 1         | Yes (API)
route              | <1ms      | 0         | No
billing handler    | ~2.5s     | 1         | Yes (API)
technical handler  | ~2.5s     | 1         | Yes (API)
general handler    | ~2.5s     | 1         | Yes (API)
format             | <1ms      | 0         | No
-------------------|-----------|-----------|-------------
Total              | ~4s       | 2         |

Optimization Opportunities:
  • Cache common classifications
  • Use streaming for real-time updates
  • Batch process multiple tickets
  • Implement prompt caching


╔══════════════════════════════════════════════════════════════════════════════╗
║                        COMPARISON: Before vs After                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

WITHOUT LANGGRAPH (Traditional Approach):
  ❌ Hardcoded if-else logic
  ❌ Difficult to visualize flow
  ❌ State management is manual
  ❌ Hard to add new categories
  ❌ Testing requires mocking entire pipeline
  ❌ No built-in observability

WITH LANGGRAPH (This Implementation):
  ✅ Declarative workflow definition
  ✅ Visual graph representation
  ✅ Automatic state management
  ✅ Easy to extend with new nodes
  ✅ Each node testable independently
  ✅ Built-in logging and monitoring

"""

    print(diagram)


if __name__ == "__main__":
    print_workflow_diagram()
