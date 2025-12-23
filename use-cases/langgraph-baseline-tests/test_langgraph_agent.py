"""
Simple test script for the LangGraph conversational agent.

This script runs a quick test to verify that:
1. The agent can be created successfully
2. Memory/checkpointing works across multiple turns
3. Thread isolation works correctly
"""

import os
from langgraph_conversational_agent import create_agent, chat, get_conversation_history


def test_memory_persistence():
    """Test that the agent remembers conversation context."""
    print("Test 1: Memory Persistence")
    print("-" * 40)

    app = create_agent()
    thread_id = "test-001"

    # First turn - introduce information
    response1 = chat(app, thread_id, "My favorite color is blue.")
    print(f"Turn 1: My favorite color is blue.")
    print(f"Response: {response1[:100]}...")

    # Second turn - test memory
    response2 = chat(app, thread_id, "What's my favorite color?")
    print(f"\nTurn 2: What's my favorite color?")
    print(f"Response: {response2}")

    # Check if the response mentions blue
    if "blue" in response2.lower():
        print("\n✓ PASSED: Agent remembered the favorite color!")
        return True
    else:
        print("\n✗ FAILED: Agent did not remember the favorite color")
        return False


def test_thread_isolation():
    """Test that different threads maintain separate conversations."""
    print("\n\nTest 2: Thread Isolation")
    print("-" * 40)

    app = create_agent()

    # Thread 1
    thread1 = "test-thread-1"
    chat(app, thread1, "My name is Alice.")

    # Thread 2
    thread2 = "test-thread-2"
    chat(app, thread2, "My name is Bob.")

    # Ask Thread 1 about the name
    response1 = chat(app, thread1, "What's my name?")
    print(f"Thread 1 response: {response1}")

    # Ask Thread 2 about the name
    response2 = chat(app, thread2, "What's my name?")
    print(f"Thread 2 response: {response2}")

    # Verify isolation
    if "alice" in response1.lower() and "bob" in response2.lower():
        print("\n✓ PASSED: Threads are properly isolated!")
        return True
    else:
        print("\n✗ FAILED: Thread isolation not working correctly")
        return False


def test_conversation_history_retrieval():
    """Test that we can retrieve conversation history."""
    print("\n\nTest 3: Conversation History Retrieval")
    print("-" * 40)

    app = create_agent()
    thread_id = "test-003"

    # Have a short conversation
    chat(app, thread_id, "Hello!")
    chat(app, thread_id, "How are you?")

    # Retrieve history
    history = get_conversation_history(app, thread_id)

    print(f"Retrieved {len(history)} messages")

    # Should have 4 messages: 2 human, 2 AI
    if len(history) == 4:
        print("\n✓ PASSED: Conversation history retrieved correctly!")
        return True
    else:
        print(f"\n✗ FAILED: Expected 4 messages, got {len(history)}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("LangGraph Conversational Agent Tests")
    print("="*60)

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it before running tests:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    try:
        results = []

        # Run tests
        results.append(test_memory_persistence())
        results.append(test_thread_isolation())
        results.append(test_conversation_history_retrieval())

        # Summary
        print("\n\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if passed == total:
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ {total - passed} test(s) failed")

    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
