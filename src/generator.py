import os
from typing import List, Dict
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(query: str, retrieved_docs: List[Dict]) -> str:
    """Build the prompt by combining retrieved context with the user's query."""
    context = "\n\n".join(
        f"[{doc['source']}]\n{doc['content']}" for doc in retrieved_docs
    )
    return f"""You are Cadence AI, a music recommendation assistant.
Use only the information provided below to answer the user's question.
Do not make up songs, artists, or facts that are not in the context.

--- CONTEXT ---
{context}
--- END CONTEXT ---

User question: {query}

Give a helpful, conversational recommendation based strictly on the context above."""


def generate(query: str, retrieved_docs: List[Dict]) -> str:
    """Send the prompt to Gemini and return the response text."""
    prompt = build_prompt(query, retrieved_docs)
    try:
        response = client.models.generate_content(
            model="gemma-3-1b-it",
            contents=prompt
        )
        return response.text
    except Exception:
        sources = ", ".join(set(doc["source"] for doc in retrieved_docs))
        return (
            f"[Demo mode — Gemini API unavailable]\n\n"
            f"Based on your query, I found relevant information in: {sources}.\n"
            f"Once the API is connected, I'll generate a full recommendation here."
        )
