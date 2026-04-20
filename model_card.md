# Model Card: Cadence AI

## Model Name
Cadence AI

## What It Does
Cadence AI is a music recommendation assistant that uses Retrieval-Augmented Generation. You describe what you want in plain English and it searches a knowledge base of genre guides, mood descriptions, and a song catalog before generating a recommendation. It only answers questions related to music and refuses to respond when it cannot find relevant information.

## Base Project
This system extends the Music Recommender Simulation from AI110 Module 3. The original project used a weighted rule-based scoring function to rank songs by genre, mood, energy, and acoustic preference. Cadence AI keeps that song catalog and adds a natural language interface, a RAG pipeline, Gemini integration, and guardrails on top.

## How It Works
When you type a question, the retriever searches the docs folder for relevant chunks using keyword matching. The top three results get passed to Gemini along with your question. Gemini is instructed to answer using only that context. If the retriever comes back empty or the question is off-topic, the guardrail blocks the request instead of letting the model guess.

## Data
The knowledge base has four sources: a genre guide covering 13 genres, a mood guide covering 15 moods, a system description doc, and a CSV of 18 songs with attributes like energy, tempo, valence, danceability, acousticness, mood tag, and release decade. The dataset is small and focused on a narrow slice of music styles, which limits how useful the system is for users with niche tastes.

## Limitations and Bias
The keyword search does not understand meaning. If you type "melancholy" it will not match documents that say "sad" even though they mean the same thing. The song catalog only has 18 songs, so most genres have one or two representatives at most. If your taste falls outside what is in the catalog, the recommendations will feel thin. The genre match in the original scoring logic also gives genre too much weight, so a song can rank high just for being the right genre even if the energy and mood are completely off.

## Evaluation
I tested the system with six predefined inputs covering music queries, off-topic queries, and nonsense inputs. All six passed. Music queries retrieved relevant docs and got through the guardrail. The off-topic query about politics was blocked immediately. The nonsense query retrieved nothing and was blocked by the empty-context check. The test harness in tests/test_system.py runs all six cases and prints a pass/fail report.

The one thing that surprised me was how well the guardrail held up on edge cases. I expected it to let some borderline queries through, but the combination of the off-topic check and the empty-retrieval check covered everything I threw at it.

## AI Collaboration
I used Claude to help write and structure the code for this project. The most helpful moment was when it suggested adding a fallback demo mode to the generator so the app would not crash when the API key had quota issues. That was a practical fix I would not have thought of immediately.

The one time it gave me a flawed suggestion was when it initially used the deprecated google.generativeai package instead of the newer google.genai package. The code ran but threw warnings and then failed when the model name changed. I had to debug that manually before figuring out the right import and client structure.

## Potential Misuse
The system is scoped to music recommendations and has a guardrail blocking off-topic queries. It cannot be used to generate harmful content because it is grounded in a fixed knowledge base and refuses to answer when context is missing. The main risk is that a user could add malicious content to the docs folder and manipulate the retrieval results, but that requires direct access to the file system.

## Future Improvements
The keyword search could be replaced with embedding-based retrieval so the system understands meaning instead of just matching words. The song catalog could be expanded to at least 100 songs across more genres. A listening history feature would let the system track what you have already heard and stop recommending the same songs every time.

## Personal Reflection
This project changed how I think about AI systems. Before this, I assumed the hardest part was getting the model to generate good responses. It turns out the hardest part is deciding what the system should and should not respond to, and making sure the data it works with is actually reliable. The RAG pipeline makes the system honest in a way that a plain LLM call cannot be, because it cannot recommend something that is not in the knowledge base. That tradeoff between flexibility and reliability is something I will think about whenever I use AI tools going forward.
