from pathlib import Path
from retriever.hybrid_retriever import load_indexes
from retriever.hybrid_retriever import hybrid_retrieve
from retriever.reranker import rerank
from pipelines.context_builder import build_context


query = "Who is the Executive Chairman of the company?"
top_k = 5

VECTORSTORE_DIR = Path("vectorstore")

print("Loading indexes...")
vectorstore, bm25_data = load_indexes(VECTORSTORE_DIR)
print("Index Loaded!!!")


print("Running hybrid retrieval...")
results = hybrid_retrieve(query, vectorstore,bm25_data, top_k)

print("\n--- RRF SCORES (combined from both lanes) ---")
for i, r in enumerate(results):
    print(f"  Rank {i+1} | rrf_score: {r['score']:.5f} | {r['doc'].page_content[:70].strip()}...")
print("hybrid retrieval done!!!")


print("Reranking results...")

reranked = rerank(query, results, top_k)

print("\n--- RERANKER SCORES (after cross-encoder) ---")
for i, r in enumerate(reranked):
    print(f"  Rank {i+1} | rerank_score: {r['rerank_score']:.3f} | {r['doc'].page_content[:70].strip()}...")


print("Results reranked!!!")

print("Building context...")
context = build_context(query, reranked)
print("Context Building Done!!!")

print("\n" + "="*50)
print(f"QUERY: {query}")
print("="*50)

print(f"\nTotal chunks used: {context['num_chunks']}")

print("\n--- CONTEXT SENT TO LLM ---\n")
print(context["context_string"])


print("\n--- SOURCES ---")
for s in context["sources"]:
    print(f"  {s['source']}  |  page {s['page']}")

