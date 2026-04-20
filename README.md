# Cadence AI

A RAG-powered music recommendation assistant built on top of the Music Recommender Simulation we did in AI110 Module 3.

---

## Base Project

**Original Project:** Music Recommender Simulation (AI110 Module 3)

The Music Recommender Simulation was a rule-based recommendation engine built in Python. It scored songs from an 18-song catalog against a user's preferred genre, mood, energy level, and acoustic preference using a weighted scoring function. The system ran entirely from the command line and produced ranked recommendations with plain-English explanations for each result.

For the final project I chose to create an AI music recommender called Cadence AI which extends that foundation by adding a natural language interface, a RAG pipeline that retrieves music knowledge before generating any response, a Gemini-powered generator, and a Streamlit User Interface. It turns the CLI script we used and demonstrated in Module 3 into a full applied AI system.

---

## What It Does

Cadence AI is an AI that lets you describe what you're in the mood for listening in plain English and returns a grounded and accurate music recommendation. Instead of filling out the user's preference fields, the user can just type something like:

- *"suggest something chill and acoustic for studying"*
- *"I want high energy pop for working out"*
- *"something dark and moody for a night drive"*

Then the system searches a real knowledge base of genre guides, mood descriptions, and the song catalog before calling the AI so every answer is grounded in actual data instead of being made up.

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

## Sample Interactions with Cadence AI

![Cadence AI Demo](assets/demo_screenshot.png)

**Input:** *"suggest something chill and acoustic for late night studying"*

> Based on your query, I found lofi and acoustic tracks that match well. Midnight Coding by LoRoom is a great pick. It's lofi with chill energy (0.42) and high acousticness (0.71), perfect for a focused late-night session. Library Rain by Paper Lanterns is another strong option with an even softer feel.

---

**Input:** *"I want something intense and high energy for the gym"*

> For the gym, Storm Runner by Voltline stands out. It's rock with intense mood and energy of 0.91 at 152 BPM. If you want something more electronic, Bass Drop by Circuit Nine hits 0.96 energy at 140 BPM with an aggressive mood tag.

---

**Input:** *"what do you think about politics"* (guardrail test)

> 🚫 I can only help with music recommendations. That topic is outside my scope.

![Guardrail Demo](assets/guardrail.png)

---

## Design Decisions

**Why use RAG instead of just prompting Gemini directly?**
Without retrieval, the model would make up song titles and artist names but by grounding every response in the actual docs and song catalog, the system can only recommend songs that actually exist.

**Why keyword search instead of embeddings?**
Embeddings would require an additional API or the use of another library. Keyword matching is fast and easy to explain which matters more for a class projects rather than raw accuracy.

**Why use a guardrail?**
A guardrail that refuses to answer when context is missing is more honest than a wrong answer that sounded too confident. I also believe it demonstrates a responsible AI design.

**Why use Streamlit?**
I used streamlit because it turns the CLI script into something anyone can demo without knowing how to work with Python which matters for the presentation while demo time.

---

## Testing Summary

The test harness in `tests/test_system.py` runs 6 predefined inputs through the retriever and the guardrail and it prints a pass/fail report.

- Music queries such as lofi, pop, rock, moody, all retrieved relevant docs and passed the guardrail.
- Off-topic queries like politics, were correctly blocked by the guardrail.
- Queries that didn't make any sense, retrieved nothing and was blocked so the system correctly refused to answer the question.

**Result: 6/6 tests passed. The guardrail correctly blocked all off-topic and empty-context queries. The system struggled with synonym mismatches since keyword search cannot match "melancholy" to "sad" even though they mean the same thing. Logging captured every interaction including guardrail rejections which made it easy to trace exactly what the system did and why.**

---

## Reflection

Building Cadence AI showed me that retrieval is often more important than generation. I learned that Gemini is capable of producing convincing music recommendations from nothing but those recommendations would be made up. The RAG layer is what makes the system trustworthy because it forces the model to work with real data.

The hardest part was deciding what the system should refuse to do AKA the guardrails. A guardrail that fires too often is useless and one that fires too rarely defeats the purpose. Getting that balance to work and make it right required me to actually test the edge cases instead of just assuming the simpler path would work.

---

## Loom Walkthrough


---

## Base Project Reference

- Module 3 repo: [ai110-module3show-musicrecommendersimulation-starter](https://github.com/fikirzelalem/ai110-module3show-musicrecommendersimulation-starter)
- Original scoring logic reused in: `src/retriever.py` (song loading pattern)
- Original dataset reused in: `docs/songs.csv`

---

## Portfolio Reflection

Building Cadence AI showed me that I can take a any idea and turn it into something real. I started with a basic rule-based music recommender and ended up with a full applied AI system that retrieves knowledge, it checks its own work before answering, logs every interaction, and explains its reasonings as to why step by step. That progression matters to me because it shows I can build things that are not just functional but also things that are responsible.

What this project says about me as an AI engineer is that I care about how a system behaves and not just whether it runs on the system. I spent more time thinking about what the system should refuse to do than on any other part of the build. I think that mindset is something I want to carry into every AI project I work on going forward.

---

*Built by Fikir Demeke | AI110 Final Project*
