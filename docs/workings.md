# How MoodMix AI Works

## Overview
MoodMix AI is a music recommendation assistant that uses Retrieval-Augmented Generation (RAG). Instead of relying purely on an AI model to guess what songs you might like, it first searches a real knowledge base of music information and then uses that evidence to generate a recommendation.

## Step 1: You Ask a Question
You type a natural language question like "what should I listen to when I'm studying late at night?" or "suggest something chill and acoustic."

## Step 2: Retrieval
The system searches through the docs folder which contains genre guides, mood descriptions, artist profiles, and the full song catalog. It finds the most relevant chunks of information based on the words in your query.

## Step 3: Guardrail Check
Before calling the AI, the system checks two things:
- Is the question music-related? If not, it refuses to answer.
- Did the retrieval find anything useful? If not, it says it doesn't know rather than making something up.

## Step 4: Generation
The retrieved context gets passed to Gemini along with your question. Gemini is instructed to answer using only the provided context. This prevents hallucination.

## Step 5: Logging
Every interaction is saved to a log file so you can review what the system answered, what it retrieved, and whether the guardrail fired.

## Scoring System (from base project)
Songs are scored using weighted features:
- Genre match: +2 to +3 points
- Mood match: +1 to +3 points
- Energy closeness: up to +1 point based on how close the song energy is to your preference
- Acoustic bonus: +0.5 if you like acoustic and the song is acoustic
- Popularity, decade, mood tag, explicit penalty, and live feel bonuses also available
