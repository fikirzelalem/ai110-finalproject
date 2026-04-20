import streamlit as st
from src.retriever import load_docs, load_songs_as_docs, retrieve
from src.guardrail import check
from src.generator import generate
from src.logger import log

st.set_page_config(page_title="Cadence AI", page_icon="🎵", layout="centered")

# Sidebar
with st.sidebar:
    st.title("About Cadence AI")
    st.markdown("""
Cadence AI is a music recommendation assistant that uses **Retrieval-Augmented Generation (RAG)**.

Instead of guessing, it searches a real knowledge base of genres, moods, and songs before generating a recommendation.

**How it works:**
1. You describe what you want
2. The system searches the knowledge base
3. A guardrail checks if the question is valid
4. Gemini generates a grounded response

**Knowledge base includes:**
- 13 genre guides
- 15 mood descriptions
- 18 songs with full metadata
""")
    st.divider()
    st.caption("Built for AI110 Module 4")
    st.caption("Extends the Music Recommender Simulation (Module 3)")

# Main content
st.title("🎵 Cadence AI")
st.markdown("##### Your RAG-powered music recommendation assistant")
st.markdown("Describe your mood or what you're looking for and get a recommendation grounded in real data.")

st.divider()

@st.cache_resource
def load_all_docs():
    docs = load_docs("docs")
    docs += load_songs_as_docs("docs/songs.csv")
    return docs

docs = load_all_docs()

# Quick prompt buttons
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

st.markdown("**Try one of these:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Chill study vibes"):
        st.session_state.query_input = "something chill and acoustic for studying"
with col2:
    if st.button("Gym energy"):
        st.session_state.query_input = "high energy intense song for the gym"
with col3:
    if st.button("Late night drive"):
        st.session_state.query_input = "something moody and dark for a night drive"

st.markdown("")

query = st.text_input("Or type your own:", value=st.session_state.query_input, placeholder="e.g. suggest something chill and acoustic")

if st.button("Get Recommendation", type="primary") and query.strip():
    with st.spinner("Searching knowledge base..."):
        retrieved = retrieve(query, docs, top_k=3)

    guardrail_passed, reason = check(query, retrieved)

    if not guardrail_passed:
        st.warning(f"🚫 {reason}")
        log(query, retrieved, reason, guardrail_passed=False)
    else:
        with st.spinner("Generating recommendation..."):
            response = generate(query, retrieved)

        st.success("Here's what I found:")
        st.markdown("### 🎧 Recommendation")
        st.write(response)

        with st.expander("📄 Sources used by the retriever"):
            for doc in retrieved:
                st.markdown(f"**{doc['source']}**")
                st.caption(doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"])

        log(query, retrieved, response, guardrail_passed=True)

st.divider()
st.caption("Built by Fikir Demeke | AI110 Module 4 Final Project | Powered by Gemini")
