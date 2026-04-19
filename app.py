import streamlit as st
from src.retriever import load_docs, load_songs_as_docs, retrieve
from src.guardrail import check
from src.generator import generate
from src.logger import log

st.set_page_config(page_title="MoodMix AI", page_icon="🎵", layout="centered")

st.title("🎵 MoodMix AI")
st.caption("A RAG-powered music recommendation assistant built on the Music Recommender (Module 3)")

@st.cache_resource
def load_all_docs():
    docs = load_docs("docs")
    docs += load_songs_as_docs("docs/songs.csv")
    return docs

docs = load_all_docs()

st.markdown("### Ask me anything about music")
st.markdown("Try: *'what should I listen to when studying late at night?'* or *'suggest something high energy and happy'*")

query = st.text_input("Your question:", placeholder="e.g. suggest something chill and acoustic")

if st.button("Get Recommendation") and query.strip():
    with st.spinner("Searching knowledge base..."):
        retrieved = retrieve(query, docs, top_k=3)

    guardrail_passed, reason = check(query, retrieved)

    if not guardrail_passed:
        st.warning(f"🚫 {reason}")
        log(query, retrieved, reason, guardrail_passed=False)
    else:
        with st.spinner("Generating recommendation..."):
            response = generate(query, retrieved)

        st.markdown("### 🎧 Recommendation")
        st.write(response)

        with st.expander("📄 Sources used"):
            for doc in retrieved:
                st.markdown(f"**{doc['source']}**")
                st.caption(doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"])

        log(query, retrieved, response, guardrail_passed=True)

st.divider()
st.caption("Built by extending the Music Recommender Simulation (AI110 Module 3) | Powered by Gemini")
