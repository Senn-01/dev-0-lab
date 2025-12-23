"""
Customer Support Ticket Workflow using LangGraph

This workflow demonstrates:
1. Ticket classification (billing, technical, general)
2. Conditional routing based on classification
3. Specialized handlers for each ticket type
4. Final response formatting
"""

import os
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, END
from anthropic import Anthropic


# State definition - this is passed through the entire workflow
class TicketState(TypedDict):
    """State object that flows through the graph"""
    ticket_id: str
    ticket_content: str
    classification: str
    handler_response: str
    formatted_response: str


# Initialize Anthropic client
def get_anthropic_client():
    """Initialize Anthropic client with API key from environment"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)


# Node 1: Classify the ticket
def classify_ticket(state: TicketState) -> TicketState:
    """
    Classifies the support ticket into one of three categories:
    - billing: Payment, invoices, subscription issues
    - technical: Product bugs, performance, technical errors
    - general: General inquiries, questions, feedback
    """
    client = get_anthropic_client()

    prompt = f"""Analyze this customer support ticket and classify it into one of these categories:
- billing: For payment, invoices, refunds, subscription issues
- technical: For bugs, errors, performance issues, technical problems
- general: For general questions, feedback, or other inquiries

Ticket content: {state['ticket_content']}

Respond with ONLY the category name (billing, technical, or general), nothing else."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=50,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    classification = message.content[0].text.strip().lower()

    # Ensure classification is valid
    if classification not in ["billing", "technical", "general"]:
        classification = "general"  # Default fallback

    state["classification"] = classification
    print(f"[CLASSIFY] Ticket {state['ticket_id']} classified as: {classification}")

    return state


# Node 2a: Handle billing tickets
def handle_billing(state: TicketState) -> TicketState:
    """Generates a response for billing-related tickets"""
    client = get_anthropic_client()

    prompt = f"""You are a billing support specialist. A customer has submitted this billing inquiry:

{state['ticket_content']}

Provide a helpful, professional response that:
1. Acknowledges their concern
2. Provides relevant information about billing processes
3. Offers next steps or solutions
4. Mentions escalation to the billing team if needed

Keep the response concise (2-3 paragraphs)."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    state["handler_response"] = message.content[0].text.strip()
    print(f"[BILLING HANDLER] Generated response for ticket {state['ticket_id']}")

    return state


# Node 2b: Handle technical tickets
def handle_technical(state: TicketState) -> TicketState:
    """Generates a response for technical support tickets"""
    client = get_anthropic_client()

    prompt = f"""You are a technical support specialist. A customer has reported this technical issue:

{state['ticket_content']}

Provide a helpful, professional response that:
1. Acknowledges the technical issue
2. Suggests troubleshooting steps or workarounds
3. Asks for additional information if needed (error logs, screenshots, etc.)
4. Sets expectations for resolution timeline

Keep the response concise (2-3 paragraphs)."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    state["handler_response"] = message.content[0].text.strip()
    print(f"[TECHNICAL HANDLER] Generated response for ticket {state['ticket_id']}")

    return state


# Node 2c: Handle general tickets
def handle_general(state: TicketState) -> TicketState:
    """Generates a response for general inquiry tickets"""
    client = get_anthropic_client()

    prompt = f"""You are a customer support representative. A customer has submitted this general inquiry:

{state['ticket_content']}

Provide a helpful, professional response that:
1. Acknowledges their message
2. Answers their questions or provides relevant information
3. Offers additional resources or assistance
4. Thanks them for reaching out

Keep the response concise (2-3 paragraphs)."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    state["handler_response"] = message.content[0].text.strip()
    print(f"[GENERAL HANDLER] Generated response for ticket {state['ticket_id']}")

    return state


# Node 3: Format the final response
def format_response(state: TicketState) -> TicketState:
    """Formats the final response with professional email template"""
    formatted = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOMER SUPPORT RESPONSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ticket ID: {state['ticket_id']}
Category: {state['classification'].upper()}

Dear Valued Customer,

{state['handler_response']}

Best regards,
Customer Support Team
Support Ticket: {state['ticket_id']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    state["formatted_response"] = formatted
    print(f"[FORMAT] Formatted final response for ticket {state['ticket_id']}")

    return state


# Routing function: decides which handler to use based on classification
def route_ticket(state: TicketState) -> Literal["billing", "technical", "general"]:
    """
    Conditional routing function that directs the ticket to the appropriate handler
    based on its classification.
    """
    classification = state["classification"]
    print(f"[ROUTE] Routing ticket {state['ticket_id']} to {classification} handler")
    return classification


# Build the workflow graph
def build_workflow() -> StateGraph:
    """
    Constructs the LangGraph workflow with all nodes and edges.

    Graph structure:
    START -> classify_ticket -> route_ticket -> {billing|technical|general}_handler -> format_response -> END
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(TicketState)

    # Add all nodes
    workflow.add_node("classify", classify_ticket)
    workflow.add_node("billing", handle_billing)
    workflow.add_node("technical", handle_technical)
    workflow.add_node("general", handle_general)
    workflow.add_node("format", format_response)

    # Set the entry point
    workflow.set_entry_point("classify")

    # Add conditional routing from classify to handlers
    workflow.add_conditional_edges(
        "classify",
        route_ticket,
        {
            "billing": "billing",
            "technical": "technical",
            "general": "general"
        }
    )

    # All handlers lead to format node
    workflow.add_edge("billing", "format")
    workflow.add_edge("technical", "format")
    workflow.add_edge("general", "format")

    # Format node leads to END
    workflow.add_edge("format", END)

    return workflow


# Main execution function
def process_ticket(ticket_id: str, ticket_content: str) -> dict:
    """
    Process a customer support ticket through the workflow.

    Args:
        ticket_id: Unique identifier for the ticket
        ticket_content: The customer's message/issue description

    Returns:
        Final state dict containing all processing results
    """
    print(f"\n{'='*60}")
    print(f"Processing Ticket: {ticket_id}")
    print(f"{'='*60}\n")

    # Build and compile the workflow
    workflow = build_workflow()
    app = workflow.compile()

    # Initialize the state
    initial_state: TicketState = {
        "ticket_id": ticket_id,
        "ticket_content": ticket_content,
        "classification": "",
        "handler_response": "",
        "formatted_response": ""
    }

    # Run the workflow
    final_state = app.invoke(initial_state)

    return final_state


def visualize_graph():
    """
    Visualizes the workflow graph structure.
    Requires: pip install pygraphviz (optional)
    """
    try:
        from IPython.display import Image, display

        workflow = build_workflow()
        app = workflow.compile()

        # Generate graph visualization
        graph_image = app.get_graph().draw_mermaid_png()

        # Display in Jupyter or save to file
        with open("/Users/cedricsecondo/SandBox/wip/claude-skills-lab/workflow_graph.png", "wb") as f:
            f.write(graph_image)

        print("Graph visualization saved to: workflow_graph.png")

    except ImportError:
        print("Graph visualization requires IPython and graphviz libraries")
        print("\nGraph structure (text representation):")
        print("""
        START
          │
          ▼
    ┌─────────────┐
    │  classify   │
    └─────────────┘
          │
          ▼
    ┌─────────────┐
    │    route    │ (conditional)
    └─────────────┘
       │  │  │
       │  │  └──────┐
       │  └────┐    │
       ▼       ▼    ▼
    ┌────┐ ┌────┐ ┌────┐
    │bill│ │tech│ │gen │
    └────┘ └────┘ └────┘
       │       │    │
       └───┬───┘    │
           │        │
           ▼        ▼
       ┌─────────────┐
       │   format    │
       └─────────────┘
           │
           ▼
          END
        """)


# Example usage and test cases
if __name__ == "__main__":
    # Test case 1: Billing issue
    print("\n" + "="*60)
    print("TEST CASE 1: BILLING ISSUE")
    print("="*60)

    result1 = process_ticket(
        ticket_id="TKT-001",
        ticket_content="I was charged twice for my subscription this month. Can you please refund the duplicate charge?"
    )
    print("\n" + result1["formatted_response"])

    # Test case 2: Technical issue
    print("\n" + "="*60)
    print("TEST CASE 2: TECHNICAL ISSUE")
    print("="*60)

    result2 = process_ticket(
        ticket_id="TKT-002",
        ticket_content="The app keeps crashing whenever I try to upload a file larger than 10MB. Error code: ERR_TIMEOUT"
    )
    print("\n" + result2["formatted_response"])

    # Test case 3: General inquiry
    print("\n" + "="*60)
    print("TEST CASE 3: GENERAL INQUIRY")
    print("="*60)

    result3 = process_ticket(
        ticket_id="TKT-003",
        ticket_content="What are your business hours? I'd like to schedule a demo of your premium features."
    )
    print("\n" + result3["formatted_response"])

    # Show graph structure
    print("\n" + "="*60)
    print("WORKFLOW GRAPH STRUCTURE")
    print("="*60)
    visualize_graph()
