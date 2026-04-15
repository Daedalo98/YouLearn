import streamlit as st

# 1. Initialize Page Configuration globally
st.set_page_config(layout="wide", page_title="Educational Pipeline", page_icon="🎓")

# 2. Define our Multi-Page App structure
yt_page = st.Page("pages/youtube.py", title="YouTube Pipeline", icon="🎥")
pdf_page = st.Page("pages/pdf.py", title="PDF Pipeline", icon="📄")
websites_page = st.Page("pages/websites.py", title="Web Scraping Pipeline", icon="🌐")
rag_page = st.Page("pages/advanced_rag.py", title="Advanced RAG Configurator", icon="🧠")

# 3. Setup Modern Navigation
pg = st.navigation([yt_page, pdf_page, websites_page, rag_page])

# 4. State Safety: Context Switching
# We track which page the user is currently on.
if "current_context" not in st.session_state:
    st.session_state.current_context = "startup"

# If the user switches pages, we clear the shared downstream variables
current_page = pg.title
if st.session_state.current_context != current_page:
    st.session_state.current_context = current_page
    
    # List of shared variables used by the LLM and Quiz engine to clear on switch
    keys_to_clear = [
        "enhanced_text", "is_editing_enhanced", "quiz_state", "q_list", 
        "evaluations", "a_model_data", "bg_thread_status", "q_index", 
        "quiz_score", "regenerated_indices", "q_payload_log"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# 5. Run the selected page
pg.run()