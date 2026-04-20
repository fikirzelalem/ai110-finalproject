# Cadence AI

A RAG-powered music recommendation assistant built on top of the Music Recommender Simulation (AI110 Module 3).

---

## Base Project

**Original Project:** Music Recommender Simulation (AI110 Module 3)

The Music Recommender Simulation was a rule-based recommendation engine built in Python. It scored songs from an 18-song catalog against a user's preferred genre, mood, energy level, and acoustic preference using a weighted scoring function. The system ran entirely from the command line and produced ranked recommendations with plain-English explanations for each result.

Cadence AI extends that foundation by adding a natural language interface, a RAG pipeline that retrieves music knowledge before generating a response, a Gemini-powered generator, and a Streamlit UI. It turns a CLI script into a full applied AI system.

---

## What It Does

Cadence AI lets you describe what you're in the mood for in plain English and returns a grounded music recommendation. Instead of filling out preference fields, you just type something like:

- *"suggest something chill and acoustic for studying"*
- *"I want high energy pop for working out"*
- *"something dark and moody for a night drive"*

The system searches a real knowledge base of genre guides, mood descriptions, and the song catalog before calling the AI, so every answer is grounded in actual data instead of hallucinated.

---

## System Architecture

![Cadence AI Architecture](assets/architecture.png)

```
User Input (Streamlit UI)
        │
        ▼
┌─────────────────┐
│   Retriever     │ ← searches docs/ folder (genres.md, moods.md, workings.md, songs.csv)
└────────┬────────┘
         │ top-3 relevant chunks
         ▼
┌─────────────────┐
│   Guardrail     │ ← blocks off-topic queries and empty retrievals
└────────┬────────┘
         │ if passed
         ▼
┌─────────────────┐
│   Generator     │ ← sends context + query to Gemini, returns grounded response
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Logger       │ ← saves every interaction to logs/interactions.jsonl
└────────┬────────┘
         │
         ▼
   Streamlit UI displays response + sources used
```

---

## Setup Instructions

**1. Clone the repo**
```bash
git clone https://github.com/fikirzelalem/applied-ai-system-project.git
cd applied-ai-system-project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

**4. Run the app**
```bash
streamlit run app.py
```

**5. Run the test harness**
```bash
python -m tests.test_system
```

---

## Sample Interactions

**Input:** *"suggest something chill and acoustic for late night studying"*

> Based on your query, I found lofi and acoustic tracks that match well. Midnight Coding by LoRoom is a great pick. It's lofi with chill energy (0.42) and high acousticness (0.71), perfect for a focused late-night session. Library Rain by Paper Lanterns is another strong option with an even softer feel.

---

**Input:** *"I want something intense and high energy for the gym"*

> For the gym, Storm Runner by Voltline stands out. It's rock with intense mood and energy of 0.91 at 152 BPM. If you want something more electronic, Bass Drop by Circuit Nine hits 0.96 energy at 140 BPM with an aggressive mood tag.

---

**Input:** *"what do you think about politics"* (guardrail test)

> 🚫 I can only help with music recommendations. That topic is outside my scope.

---

## Design Decisions

**Why RAG instead of just prompting Gemini directly?**
Without retrieval, the model would hallucinate song titles and artist names. By grounding every response in the actual docs and song catalog, the system can only recommend songs that actually exist.

**Why keyword search instead of embeddings?**
Embeddings would require an additional API or library. Keyword matching is transparent, fast, and easy to explain, which matters more for a classroom project than raw accuracy.

**Why a guardrail?**
A guardrail that refuses to answer when context is missing is more honest than a confident wrong answer. It also demonstrates responsible AI design.

**Why Streamlit?**
It turns a CLI script into something anyone can demo without knowing Python, which matters for a science fair presentation.

---

## Testing Summary

The test harness in `tests/test_system.py` runs 6 predefined inputs through the retriever and guardrail and prints a pass/fail report.

- Music queries (lofi, pop, rock, moody): all retrieved relevant docs and passed the guardrail
- Off-topic query (politics): correctly blocked by the guardrail
- Nonsense query: retrieved nothing and was blocked, so the system correctly refused to answer

**Result: 6/6 tests passed**

The biggest limitation is that keyword search misses synonyms. "melancholy" won't match "sad" even if they mean the same thing.

---

## Reflection

Building Cadence AI showed me that retrieval is often more important than generation. Gemini is capable of producing convincing music recommendations from nothing, but those recommendations would be made up. The RAG layer is what makes the system trustworthy because it forces the model to work with real data.

The hardest part was not the code, it was deciding what the system should refuse to do. A guardrail that fires too often is useless, and one that fires too rarely defeats the purpose. Getting that balance right required actually testing edge cases instead of just assuming the happy path would work.

---

## Loom Walkthrough

[Video link coming soon]

---

## Base Project Reference

- Module 3 repo: [ai110-module3show-musicrecommendersimulation-starter](https://github.com/fikirzelalem/ai110-module3show-musicrecommendersimulation-starter)
- Original scoring logic reused in: `src/retriever.py` (song loading pattern)
- Original dataset reused in: `docs/songs.csv`

---

*Built by Fikir Demeke | AI110 Module 4 Final Project*
