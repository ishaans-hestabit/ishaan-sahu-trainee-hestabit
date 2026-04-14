SIMILARITY_MIN_SCORE = 0.25    
IMAGE_MIN_SIMILARITY = 0.70
HALLUCINATION_MAX    = 0.40


def check_text_confidence(text_results: list) -> dict:
    
    if not text_results:
        return {
            "ok":      False,
            "score":   0.0,
            "message": "I could not find any relevant documents for your question."
        }

    similarities = []
    for r in text_results:
        if isinstance(r, dict) and "faiss_similarity" in r:
            similarities.append(float(r["faiss_similarity"]))


    if not similarities:
        return {
            "ok":      True,
            "score":   0.0,
            "message": "Relevant documents found (similarity data not available)."
        }

    best_score = max(similarities)

    if best_score < SIMILARITY_MIN_SCORE:
        return {
            "ok":      False,
            "score":   round(best_score, 3),
            "message": (
                "I found some documents but none are closely related to your question. "
                "I do not have enough relevant information to give you a reliable answer."
            )
        }

    return {
        "ok":      True,
        "score":   round(best_score, 3),
        "message": "Relevant documents found."
    }


def check_image_confidence(image_results: list) -> dict:
    if not image_results:
        return {
            "ok":      False,
            "score":   0.0,
            "message": "No images found in the knowledge base."
        }

    best_score = max(r.get("similarity", 0.0) for r in image_results)

    if best_score < IMAGE_MIN_SIMILARITY:
        return {
            "ok":      False,
            "score":   round(best_score, 4),
            "message": (
                f"The closest image match has a similarity of {best_score:.0%}, "
                "which is too low to be relevant. "
                "I do not have a similar image in my knowledge base."
            )
        }

    return {
        "ok":      True,
        "score":   round(best_score, 4),
        "message": "Similar images found."
    }


def check_hallucination(answer: str, context: str) -> dict:
    STOP_WORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "will", "would", "could",
        "to", "of", "in", "on", "at", "by", "for", "with", "and",
        "or", "but", "that", "this", "it", "not", "i", "you", "we",
        "they", "their", "from", "as", "its", "also", "about", "more"
    }

    def clean_words(text):
        return set(
            w.lower().strip(".,!?;:\"'()")
            for w in text.split()
            if w.lower().strip(".,!?;:\"'()") not in STOP_WORDS and len(w) > 2
        )

    answer_words  = clean_words(answer)
    context_words = clean_words(context)

    if not answer_words:
        return {"ok": True, "score": 1.0, "message": "Empty answer."}

    overlap = answer_words & context_words
    score   = len(overlap) / len(answer_words)

    if score < HALLUCINATION_MAX:
        return {
            "ok":      False,
            "score":   round(score, 3),
            "message": (
                f"This answer may contain information not found in the documents "
                f"(faithfulness: {score:.0%}). Please verify before relying on it."
            )
        }

    return {
        "ok":      True,
        "score":   round(score, 3),
        "message": f"Answer is grounded in the retrieved documents (faithfulness: {score:.0%})."
    }