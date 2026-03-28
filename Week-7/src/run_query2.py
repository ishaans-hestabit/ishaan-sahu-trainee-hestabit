from retriever.multimodal_retriever import retrieve

if __name__ == "__main__":

    # ── TEXT QUERY 
    print("\n" + "="*55)
    print("TEST 1: Text query")
    print("="*55)
    result = retrieve("Who is the president of the company?")

    print("\n--- CONTEXT FOR LLM ---")
    print(result["context"])
    print(f"\nSources: {result['sources']}")

    # ── IMAGE QUERY
    # print("\n" + "="*55)
    # print("TEST 2: Image query")
    # print("="*55)
    # result = retrieve("data/raw/images/cat.jpeg")

    # print("\n--- CONTEXT FOR LLM ---")
    # print(result["context"])
    # print(f"\nDerived text query: {result.get('derived_query', '')}")