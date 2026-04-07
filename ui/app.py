import streamlit as st
import os
import sys

# Ensure Python knows where GyaanSetu home is
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# --- REAL BACKEND IMPORTS ---
from config import settings
from vector_store.faiss_loader import FAISSLoader
from llm.llm_factory import LLMFactory
from llm.prompt_builder import PromptBuilder
from rag.rag_service import RAGService

# ==============================
# SEO & PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="GyaanSetu | NCERT AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <head>
        <meta name="description" content="GyaanSetu is an AI-powered educational tutor specifically designed for CBSE and NCERT Class 9 and Class 10 Science and Math students.">
    </head>
""", unsafe_allow_html=True)

# ==============================
# CUSTOM CSS & BACKGROUND
# ==============================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Grid Background */
    .stApp {
        background-color: var(--background-color);
        background-image: radial-gradient(var(--text-color) 1px, transparent 1px);
        background-size: 30px 30px;
        background-position: 0 0, 15px 15px;
        background-repeat: repeat;
        opacity: 0.95;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        color: var(--text-color);
        text-align: center;
        padding: 10px; font-size: 14px; z-index: 999;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .footer a { color: #3b82f6; text-decoration: none; margin: 0 15px; font-weight: 500; }
    .footer a:hover { text-decoration: underline; }

    footer {visibility: hidden;} /* Hides default footer */
    </style>
    """, unsafe_allow_html=True)

# ==============================
# 🧠 BACKEND CONNECTION
# ==============================
@st.cache_resource(show_spinner=False)
def load_rag_tutor(class_name):
    """
    Loads the LLM and FAISS index ONLY ONCE and caches it in RAM.
    If the user changes classes, it will build and cache the new class.
    """
    # Convert "Class 9" -> 9
    class_id = int(class_name.split()[1])

    # Force settings to match the UI selection
    settings.CLASS_ID = class_id

    # Build the Engine
    vector_store = FAISSLoader()
    llm_client = LLMFactory.create()
    prompt_builder = PromptBuilder()

    rag = RAGService(
        vector_store=vector_store,
        llm_client=llm_client,
        prompt_builder=prompt_builder
    )
    return rag

# ==============================
# 🖥️ MAIN UI BUILDER
# ==============================
def main():
    inject_custom_css()

    # --- SESSION STATE (Memory) ---
    # MUST be declared before we try to loop through it
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am GyaanSetu, your NCERT AI Tutor. What would you like to learn today?"}
        ]

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("GyaanSetu Settings")
        st.markdown("---")

        selected_class = st.selectbox(
            "📚 Select Standard",
            options=["Class 9", "Class 10"],
            index=1 # Defaults to Class 10
        )

        st.markdown("---")
        st.info("💡 **Theme Toggle:** Click the '⋮' in the top right -> Settings -> Theme to manually swap.")

    # --- MAIN CHAT INTERFACE ---
    st.title("GyaanSetu 🔗")
    st.caption("Local, privacy-first models running your NCERT data.")

    # 1. ALWAYS render the history at the start of the script
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 2. Capture new input
    if user_query := st.chat_input(f"Ask a {selected_class} Science question..."):

        # 3. Add to state AND render it immediately
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # 4. Now handle the Assistant response
        with st.chat_message("assistant"):
            tutor = load_rag_tutor(selected_class)

            with st.status("🧠 Consulting NCERT...", expanded=False) as status:
                # We call the generator here
                response_generator = tutor.ask(user_query)
                status.update(label="✅ Ready!", state="complete")

            # 5. Stream the answer using Streamlit's built-in generator handler
            full_response = st.write_stream(response_generator)

        # 6. Save assistant message to state
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # --- FOOTER ---
    st.markdown("""
        <div class="footer">
            Built with ⚡ locally by Anand.
            <a href="https://www.linkedin.com/in/anand-raj-006a41217" target="_blank">LinkedIn</a> |
            <a href="https://github.com/anan5093" target="_blank">GitHub</a> |
            <a href="mailto:anand.ar1806@gmail.com">Email Me</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
