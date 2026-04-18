import os
import csv
from typing import List, Dict


def load_docs(docs_dir: str) -> List[Dict]:
    """Load all .md and .txt files from docs folder as searchable chunks."""
    docs = []
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({"source": filename, "content": content})
    return docs


def load_songs_as_docs(csv_path: str) -> List[Dict]:
    """Load songs.csv and convert each song into a searchable text chunk."""
    docs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (
                f"Title: {row['title']} | Artist: {row['artist']} | "
                f"Genre: {row['genre']} | Mood: {row['mood']} | "
                f"Energy: {row['energy']} | Tempo: {row['tempo_bpm']} BPM | "
                f"Mood Tag: {row['mood_tag']} | Decade: {row['release_decade']}s"
            )
            docs.append({"source": "songs.csv", "content": text})
    return docs


def score_doc(query: str, doc: Dict) -> float:
    """Score a doc by counting how many query words appear in its content."""
    query_words = set(query.lower().split())
    content_lower = doc["content"].lower()
    return sum(1 for word in query_words if word in content_lower)


def retrieve(query: str, docs: List[Dict], top_k: int = 3) -> List[Dict]:
    """Return the top_k most relevant docs for a given query."""
    scored = [(doc, score_doc(query, doc)) for doc in docs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored[:top_k] if score > 0]
