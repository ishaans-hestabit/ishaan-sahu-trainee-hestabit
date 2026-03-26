from langchain_core.documents import Document
from vectorstore.store import load_vectorstore
from embeddings.embedder import get_embedding_model
from vectorstore.bm25_store import load_bm25_data

def load_indexes(vectorstore_dir):

    embedding_model = get_embedding_model()
    vectorstore = load_vectorstore(vectorstore_dir,embedding_model)

    bm25_data = load_bm25_data(vectorstore_dir)

    return vectorstore, bm25_data


def rrf_combine(semantic_search_results, keyword_search_results, k=25):

    scores = {}

    dense_weight  = 1.5
    sparse_weight = 1.0  

    for rank, doc in enumerate(semantic_search_results):
        doc_id = doc.metadata.get("id")

        if doc_id is None:
            continue

        if doc_id not in scores:
            scores[doc_id] = {"doc": doc, "score": 0.0}

        scores[doc_id]["score"] += dense_weight * (1 / (k + rank + 1))

    for rank, (text, meta) in enumerate(keyword_search_results):
        doc_id = meta.get("id")

        if doc_id is None:
            continue

        if doc_id not in scores:
            
            scores[doc_id] = {
                "doc": Document(page_content=text, metadata=meta),
                "score": 0.0
            }

        scores[doc_id]["score"] += sparse_weight * (1 / (k + rank + 1))


    # Sort everything by combined score, highest first
    combined = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    print(scores)
    return combined


def hybrid_retrieve(query, vectorstore, bm25_data, top_k):

    fetch_k = top_k * 2
    
    dense_results = vectorstore.similarity_search(query,k = fetch_k)

    tokenized_query = query.lower().split()
    bm25_scores = bm25_data["index"].get_scores(tokenized_query)


    top_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:fetch_k]

    # for i in top_indices:
    #     print("-"*50)
    #     print(i)
    #     print("-"*50)
    sparse_results = [
        (bm25_data["texts"][i], bm25_data["metadatas"][i])
        for i in top_indices
    ]

    combined = rrf_combine(dense_results, sparse_results)

    return combined[:top_k]