import os, json
from groq import Groq
from dotenv import load_dotenv

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


def _call_judge(messages: list) -> str:

    load_dotenv(".env")
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY not found in .env file")

    client   = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()


def check_hallucination(answer: str, context: str) -> dict:

    if not answer or not answer.strip():
        return {"ok": True, "score": 1.0, "message": "Empty answer."}

    prompt = (
        "You are a strict faithfulness evaluator for a Retrieval-Augmented "
        "Generation (RAG) system.\n\n"
        "Your task: Determine whether the ANSWER is fully supported by the CONTEXT.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"ANSWER:\n{answer}\n\n"
        "Instructions:\n"
        "1. Break the ANSWER into individual factual claims.\n"
        "2. For each claim, check if it is directly supported by the CONTEXT.\n"
        "3. A claim is 'supported' if the CONTEXT contains evidence for it "
        "(exact match, paraphrase, or logical inference from the context).\n"
        "4. A claim is 'unsupported' if it introduces facts NOT found in the CONTEXT.\n"
        "5. Ignore filler phrases like 'Based on the documents' or "
        "'I don't have enough information' — only evaluate factual claims.\n"
        "6. If the answer explicitly states it cannot find information in the context, "
        "treat that as faithful (score 1.0).\n\n"
        'Respond with ONLY a JSON object in this exact format '
        '(no markdown, no code fences, no extra text):\n'
        '{"score": <float 0.0 to 1.0>, "verdict": "<faithful or unfaithful>", '
        '"reason": "<brief 1-2 sentence explanation>"}\n\n'
        'Where "score" is the fraction of factual claims that are supported '
        '(1.0 = all supported, 0.0 = none supported).'
    )

    try:
        raw = _call_judge([{"role": "user", "content": prompt}])

        
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        result  = json.loads(cleaned)
        score   = float(result.get("score", 0.0))
        score   = max(0.0, min(1.0, score))
        reason  = result.get("reason", "")

        if score < HALLUCINATION_MAX:
            return {
                "ok":      False,
                "score":   round(score, 3),
                "message": (
                    f"This answer may contain hallucinated information "
                    f"(faithfulness: {score:.0%}). {reason}"
                ),
            }

        return {
            "ok":      True,
            "score":   round(score, 3),
            "message": (
                f"Answer is grounded in the retrieved documents "
                f"(faithfulness: {score:.0%}). {reason}"
            ),
        }

    except Exception as e:
        print(f"[Hallucination Check] LLM judge failed: {e}")
        return {
            "ok":      True,
            "score":   0.0,
            "message": f"Faithfulness check unavailable ({e}). Proceed with caution.",
        }