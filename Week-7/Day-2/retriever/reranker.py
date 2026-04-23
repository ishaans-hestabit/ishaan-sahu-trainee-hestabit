from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = None

def get_reranker():
    global reranker
    if reranker is None:
        reranker = CrossEncoder(MODEL_NAME)
    return reranker

def rerank(query, results, top_k):

    if not results:
        return []

    model = get_reranker()
    
    pairs = [(query, r["doc"].page_content) for r in results]

    scores = model.predict(pairs)

    for i ,result in enumerate(results):
        result["rerank_score"] = scores[i]

    reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_k]