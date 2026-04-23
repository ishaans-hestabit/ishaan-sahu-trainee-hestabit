def build_context(query: str, results: list) -> dict:

    seen_texts = set()
    chunks_to_use = []

    for result in results:
        text = result["doc"].page_content.strip()
        
        if text not in seen_texts:
            seen_texts.add(text)
            chunks_to_use.append(result)


    context_parts = []
    sources = []

    for i, result in enumerate(chunks_to_use):
        doc = result["doc"]
        text = doc.page_content.strip()
        source = doc.metadata.get("source", "unknown")
        page   = doc.metadata.get("page", "?")

        context_parts.append(
            f"[Chunk {i+1}] From: {source}, page {page}\n{text}"
        )
        sources.append({"source": source, "page": page})

    return {
        "context_string": "\n\n---\n\n".join(context_parts),
        "sources": sources,
        "num_chunks": len(chunks_to_use)
    }