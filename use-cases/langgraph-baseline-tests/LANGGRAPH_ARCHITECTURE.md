# LangGraph Conversational Agent Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Application                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ chat(app, thread_id, message)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        LangGraph Runtime                         │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Checkpointer                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ Load state for thread_id from checkpoint storage    │  │ │
│  │  │   - Retrieves all previous messages                  │  │ │
│  │  │   - Initializes state if new thread                  │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      State Graph                            │ │
│  │                                                              │ │
│  │    START                                                     │ │
│  │      │                                                       │ │
│  │      ▼                                                       │ │
│  │  ┌────────┐                                                 │ │
│  │  │ Agent  │  ← Current state with full message history     │ │
│  │  │  Node  │                                                 │ │
│  │  └────┬───┘                                                 │ │
│  │       │                                                      │ │
│  │       ▼                                                      │ │
│  │     END                                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Checkpointer                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │ Save updated state for thread_id                     │  │ │
│  │  │   - Stores all messages (old + new)                  │  │ │
│  │  │   - Available for next invocation                    │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Return assistant's response
                                ▼
                            User sees response
```

## State Flow Through the System

### Turn 1: First Message

```
User Input: "My name is Alice"
Thread ID: "thread-1"

┌──────────────────────────────────────────────────────────┐
│ Step 1: Checkpointer Load                                │
│ - Look for thread-1 checkpoint                           │
│ - Not found (first message)                              │
│ - Initialize empty state                                 │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 2: Merge Input                                      │
│ State = {                                                │
│   messages: [HumanMessage("My name is Alice")]          │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 3: Execute Agent Node                               │
│ - Invoke LLM with messages                               │
│ - LLM returns: "Nice to meet you, Alice!"                │
│ - Add to state using add_messages reducer               │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 4: Final State                                      │
│ State = {                                                │
│   messages: [                                            │
│     HumanMessage("My name is Alice"),                    │
│     AIMessage("Nice to meet you, Alice!")                │
│   ]                                                      │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 5: Checkpointer Save                                │
│ - Save state for thread-1                                │
│ - Stored in checkpoint storage                           │
└──────────────────────────────────────────────────────────┘
```

### Turn 2: Follow-up Message (Same Thread)

```
User Input: "What's my name?"
Thread ID: "thread-1"  ← Same thread!

┌──────────────────────────────────────────────────────────┐
│ Step 1: Checkpointer Load                                │
│ - Look for thread-1 checkpoint                           │
│ - FOUND! Load saved state:                               │
│   messages: [                                            │
│     HumanMessage("My name is Alice"),                    │
│     AIMessage("Nice to meet you, Alice!")                │
│   ]                                                      │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 2: Merge Input                                      │
│ - Use add_messages reducer to append                     │
│ State = {                                                │
│   messages: [                                            │
│     HumanMessage("My name is Alice"),                    │
│     AIMessage("Nice to meet you, Alice!"),               │
│     HumanMessage("What's my name?")  ← NEW              │
│   ]                                                      │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 3: Execute Agent Node                               │
│ - Invoke LLM with ALL messages (history included)        │
│ - LLM sees full context and responds: "Your name is      │
│   Alice, as you told me earlier!"                        │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 4: Final State                                      │
│ State = {                                                │
│   messages: [                                            │
│     HumanMessage("My name is Alice"),                    │
│     AIMessage("Nice to meet you, Alice!"),               │
│     HumanMessage("What's my name?"),                     │
│     AIMessage("Your name is Alice...")  ← NEW            │
│   ]                                                      │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────┐
│ Step 5: Checkpointer Save                                │
│ - Update checkpoint for thread-1                         │
│ - Now contains 4 messages                                │
└──────────────────────────────────────────────────────────┘
```

## Thread Isolation

### Multiple Threads

```
Thread-1: "My name is Alice"
    ↓
Checkpoint Storage
    ├─ thread-1: [HumanMessage("My name is Alice"),
    │             AIMessage("Hi Alice!")]
    │
    └─ thread-2: (empty)


Thread-2: "My name is Bob"
    ↓
Checkpoint Storage
    ├─ thread-1: [HumanMessage("My name is Alice"),
    │             AIMessage("Hi Alice!")]
    │
    └─ thread-2: [HumanMessage("My name is Bob"),
                   AIMessage("Hi Bob!")]


Thread-1: "What's my name?"
    ↓
Loads thread-1 checkpoint → Knows "Alice"

Thread-2: "What's my name?"
    ↓
Loads thread-2 checkpoint → Knows "Bob"
```

## Component Interaction Diagram

```
┌─────────────┐
│   chat()    │ User-facing function
└──────┬──────┘
       │
       │ 1. Create input state with new message
       │
       ▼
┌─────────────┐
│ app.invoke()│ LangGraph runtime entry point
└──────┬──────┘
       │
       │ 2. Pass config with thread_id
       │
       ▼
┌─────────────────┐
│  Checkpointer   │ Load/Save state
└─────────┬───────┘
          │
          │ 3. Load checkpoint for thread_id
          │
          ▼
┌─────────────────┐
│  State Graph    │ Execute nodes
│                 │
│  ┌───────────┐  │
│  │   Agent   │  │ 4. Call LLM with history
│  │   Node    │  │
│  └───────────┘  │
└─────────┬───────┘
          │
          │ 5. Return updated state
          │
          ▼
┌─────────────────┐
│  Checkpointer   │ Save updated state
└─────────┬───────┘
          │
          │ 6. Save checkpoint
          │
          ▼
┌─────────────┐
│   chat()    │ Return response to user
└─────────────┘
```

## Message Flow with Reducer

### Without Reducer (WRONG)

```
Turn 1:
Input:  [HumanMessage("Hi")]
State:  [HumanMessage("Hi")]  ← Set
After:  [HumanMessage("Hi"), AIMessage("Hello")]

Turn 2:
Input:  [HumanMessage("Bye")]
State:  [HumanMessage("Bye")]  ← Replaced! History lost
After:  [HumanMessage("Bye"), AIMessage("Goodbye")]
```

### With add_messages Reducer (CORRECT)

```
Turn 1:
Input:  [HumanMessage("Hi")]
State:  [] + [HumanMessage("Hi")]  ← Append
After:  [HumanMessage("Hi"), AIMessage("Hello")]

Turn 2:
Input:  [HumanMessage("Bye")]
State:  [HumanMessage("Hi"), AIMessage("Hello")] + [HumanMessage("Bye")]
        ← Append to existing!
After:  [HumanMessage("Hi"), AIMessage("Hello"),
        HumanMessage("Bye"), AIMessage("Goodbye")]
```

## Checkpointer Storage Models

### MemorySaver (Development)

```
┌─────────────────────────────────────┐
│        Python Dictionary            │
│                                     │
│  {                                  │
│    "thread-1": State(...),          │
│    "thread-2": State(...),          │
│    ...                              │
│  }                                  │
│                                     │
│  Pros: Fast, simple                 │
│  Cons: Lost on restart              │
└─────────────────────────────────────┘
```

### SqliteSaver (Production - Single Server)

```
┌─────────────────────────────────────┐
│        SQLite Database              │
│                                     │
│  checkpoints.db                     │
│  ┌─────────────────────────────┐   │
│  │ thread_id │ checkpoint_data │   │
│  ├─────────────────────────────┤   │
│  │ thread-1  │ {...}           │   │
│  │ thread-2  │ {...}           │   │
│  └─────────────────────────────┘   │
│                                     │
│  Pros: Persistent, fast reads       │
│  Cons: Not distributed              │
└─────────────────────────────────────┘
```

### PostgresSaver (Production - Distributed)

```
┌─────────────────────────────────────┐
│      PostgreSQL Database            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Checkpoints Table          │ │
│  ├───────────────────────────────┤ │
│  │ thread_id │ checkpoint_data   │ │
│  │ timestamp │ metadata          │ │
│  └───────────────────────────────┘ │
│                                     │
│  Pros: Distributed, scalable        │
│  Cons: Requires DB infrastructure   │
└─────────────────────────────────────┘
           ▲         ▲         ▲
           │         │         │
       Server 1  Server 2  Server 3
```

## Extension Patterns

### Adding Tools

```
┌─────────────────────────────────────────────────────────┐
│                     State Graph                         │
│                                                          │
│    START                                                 │
│      │                                                   │
│      ▼                                                   │
│  ┌────────┐       Should use tool?                      │
│  │ Agent  │────────┐                                    │
│  └────────┘        │                                    │
│      │ No          │ Yes                                │
│      │             ▼                                     │
│      │         ┌────────┐                               │
│      │         │ Tools  │ Execute tool, return result   │
│      │         └────┬───┘                               │
│      │              │                                    │
│      │              └────► Back to Agent                │
│      │                                                   │
│      ▼                                                   │
│     END                                                  │
└─────────────────────────────────────────────────────────┘
```

### Adding Retrieval (RAG)

```
┌─────────────────────────────────────────────────────────┐
│                     State Graph                         │
│                                                          │
│    START                                                 │
│      │                                                   │
│      ▼                                                   │
│  ┌────────────┐  Get relevant docs                      │
│  │ Retrieval  │  from vector store                      │
│  └──────┬─────┘                                         │
│         │                                                │
│         ▼                                                │
│  ┌────────┐  Use docs as context                        │
│  │ Agent  │  for answering                              │
│  └────┬───┘                                             │
│       │                                                  │
│       ▼                                                  │
│     END                                                  │
└─────────────────────────────────────────────────────────┘
```

### Adding Summarization

```
┌─────────────────────────────────────────────────────────┐
│                     State Graph                         │
│                                                          │
│    START                                                 │
│      │                                                   │
│      ▼                                                   │
│  ┌────────────┐  Messages > threshold?                  │
│  │ Check Len  │────────┐                                │
│  └────────────┘        │                                │
│      │ No              │ Yes                             │
│      │                 ▼                                 │
│      │           ┌─────────────┐                        │
│      │           │ Summarize   │  Condense history      │
│      │           └──────┬──────┘                        │
│      │                  │                                │
│      └──────────────────┘                                │
│      │                                                   │
│      ▼                                                   │
│  ┌────────┐                                             │
│  │ Agent  │  Use (summarized) history                   │
│  └────┬───┘                                             │
│       │                                                  │
│       ▼                                                  │
│     END                                                  │
└─────────────────────────────────────────────────────────┘
```

## Key Design Principles

1. **Separation of Concerns**
   - Graph defines flow
   - Nodes define logic
   - Checkpointer handles persistence
   - State handles data

2. **Immutability**
   - State updates return new values
   - Reducers merge, not mutate
   - Thread isolation guaranteed

3. **Composability**
   - Nodes are independent
   - Easy to add/remove/reorder
   - Graph structure declarative

4. **Observability**
   - State inspectable at any point
   - History fully auditable
   - Checkpoints for debugging

5. **Scalability**
   - Thread-based concurrency
   - Checkpointer backend swappable
   - State size manageable

## Performance Characteristics

```
Operation             Complexity   Notes
─────────────────────────────────────────────────
Load checkpoint       O(1)         Hash lookup
Save checkpoint       O(n)         n = state size
Execute agent node    O(h*t)       h = history length
                                   t = tokens per message
Merge messages        O(n)         n = new messages
Get thread history    O(1)         Direct lookup
```

## Conclusion

The architecture is designed to be:
- **Simple**: Linear flow, clear responsibilities
- **Extensible**: Easy to add nodes and edges
- **Persistent**: Automatic checkpointing
- **Scalable**: Thread-based isolation
- **Observable**: Full state inspection

The key insight is that LangGraph handles the complexity of state management and persistence, allowing you to focus on the conversation logic itself.
