import streamlit as st
from src.retriever import load_docs, load_songs_as_docs, retrieve
from src.guardrail import check
from src.generator import generate
from src.logger import log

st.set_page_config(page_title="Cadence AI", page_icon="🎵", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🎵 Cadence AI")
    st.markdown("Your RAG-powered music recommendation assistant.")
    st.divider()
    st.markdown("""
**How it works:**
1. You describe what you want
2. The system searches the knowledge base
3. A guardrail checks if the question is valid
4. Gemini generates a grounded response

**Knowledge base:**
- 13 genre guides
- 15 mood descriptions
- 18 songs with full metadata
""")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Built for AI110 Module 4 | Extends Music Recommender (Module 3)")

@st.cache_resource
def load_all_docs():
    docs = load_docs("docs")
    docs += load_songs_as_docs("docs/songs.csv")
    return docs

docs = load_all_docs()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("Hey! I'm **Cadence AI**, your music recommendation assistant. Tell me what you're in the mood for and I'll find something that fits.\n\nTry something like:\n- *suggest something chill and acoustic for studying*\n- *high energy rock for the gym*\n- *something moody for a late night drive*")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📄 Sources used"):
                for source in message["sources"]:
                    st.caption(source)

# Chat input
if query := st.chat_input("What are you in the mood for?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Process and respond
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            retrieved = retrieve(query, docs, top_k=3)

        guardrail_passed, reason = check(query, retrieved)

        if not guardrail_passed:
            st.warning(f"🚫 {reason}")
            st.session_state.messages.append({"role": "assistant", "content": f"🚫 {reason}"})
            log(query, retrieved, reason, guardrail_passed=False)
        else:
            with st.spinner("Generating recommendation..."):
                response = generate(query, retrieved)

            st.markdown(response)

            sources = [f"**{doc['source']}**: {doc['content'][:200]}..." for doc in retrieved]
            with st.expander("📄 Sources used"):
                for source in sources:
                    st.caption(source)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "sources": sources
            })
            log(query, retrieved, response, guardrail_passed=True)
