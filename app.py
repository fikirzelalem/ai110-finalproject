import streamlit as st
from src.retriever import load_docs, load_songs_as_docs, retrieve
from src.guardrail import check
from src.generator import generate
from src.logger import log

st.set_page_config(page_title="Cadence AI", page_icon="🎵", layout="centered")

st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# Session state for quick prompts
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# Sidebar
with st.sidebar:
    st.title("🎵 Cadence AI")
    st.markdown("*Your RAG-powered music recommendation assistant*")
    st.divider()

    st.markdown("**Try a quick prompt:**")
    if st.button("🌙 Chill study night vibes"):
        st.session_state.quick_prompt = "suggest something chill and acoustic for studying"
    if st.button("💪 Gym energy"):
        st.session_state.quick_prompt = "high energy intense song for the gym"
    if st.button("🌃 Late night drive"):
        st.session_state.quick_prompt = "something moody and dark for a night drive"
    if st.button("😊 Feel good songs"):
        st.session_state.quick_prompt = "something smooth and feel good"
    if st.button("🎸 Intense rock"):
        st.session_state.quick_prompt = "intense rock song with high energy"

    st.divider()
    st.markdown("**How the AI works:**")
    st.markdown("""
1. You describe what kind of vibe you want
2. The Retriever searches the knowledge base
3. The Guardrail checks the question
4. Gemini generates a grounded response
""")
    st.divider()
    st.markdown("**Knowledge base:**")
    st.markdown("13 genres · 15 moods · 18 songs")
    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.quick_prompt = None
        st.rerun()
    st.caption("AI110 Module 4 | Cadence AI")

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

# Handle quick prompt from sidebar
if st.session_state.quick_prompt:
    query = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
else:
    query = None

# Chat input
if typed := st.chat_input("What are you in the mood for?"):
    query = typed

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Process and respond with observable agentic steps
    with st.chat_message("assistant"):
        steps = st.container()

        with steps:
            # Step 1: Retrieval
            with st.spinner("🔍 Step 1: Searching knowledge base..."):
                retrieved = retrieve(query, docs, top_k=3)
            st.caption(f"✅ Step 1 complete: found {len(retrieved)} relevant source(s)")

            # Step 2: Guardrail
            with st.spinner("🛡️ Step 2: Running guardrail check..."):
                guardrail_passed, reason = check(query, retrieved)

            if not guardrail_passed:
                st.caption("🚫 Step 2 complete: guardrail blocked this query")
                st.warning(f"🚫 {reason}")
                st.session_state.messages.append({"role": "assistant", "content": f"🚫 {reason}"})
                log(query, retrieved, reason, guardrail_passed=False)
            else:
                st.caption("✅ Step 2 complete: guardrail passed")

                # Step 3: Generation
                with st.spinner("🤖 Step 3: Generating recommendation..."):
                    response = generate(query, retrieved)
                st.caption("✅ Step 3 complete: response ready")

                st.divider()
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
