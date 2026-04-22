# MEMORY-SYSTEM.md

## Three Types of Memory

Short-term (SessionMemory)
  Stores: Current conversation messages in a Python list
  Lives: Only during this run of the program
  Used for: Keeping track of what was said in this session
  Max size: 10 messages (memory window)

Long-term (SQLite)
  Stores: Important facts extracted from conversations
  Lives: Forever in long_term.db file on disk
  Used for: Remembering things across different sessions
  File: memory/long_term.db

Vector Memory (FAISS)
  Stores: Past conversations as mathematical vectors
  Lives: Persists in memory/vectors.index file
  Used for: Finding similar past conversations by meaning
  Model: all-MiniLM-L6-v2 (local, no API needed)

## How Memory is Used

Every query goes through this flow:
1. Convert query to vector
2. Search FAISS for top 3 similar past conversations
3. Load recent facts from SQLite
4. Load last 10 messages from session memory
5. Build a prompt with all this context
6. Agent answers with full memory context
7. Save query+answer to all three stores

## Episodic vs Semantic Memory

Episodic memory = memory of specific events
  "Last time you asked about Laptop sales"
  This is what vector store stores — specific past conversations

Semantic memory = general knowledge and facts
  "The user is interested in sales data"
  This is what SQLite long-term store saves — extracted facts

## Install

pip install faiss-cpu sentence-transformers

## Run

export GROQ_API_KEY=your_key_here
python main.py