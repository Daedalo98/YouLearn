import streamlit as st
import streamlit.components.v1 as components
import os

# Import your shared UI components and the new scraper
from shared_ui import render_enhancement_step, render_quiz_step
import AI_manager as manager

# We need get_url_hash to safely save our edits back to the cache
from functions import scrape_website_to_markdown, get_url_hash

# Define the local cache directory
BASE_WEB_DIR = "saved_websites"
os.makedirs(BASE_WEB_DIR, exist_ok=True)

# --- STATE INITIALIZATION ---
@st.cache_resource
def get_manager(): 
    return manager.Manager()
ai_manager = get_manager()

# Initialize core variables for the website page
if "web_markdown" not in st.session_state:
    st.session_state.web_markdown = ""
if "web_url" not in st.session_state:
    st.session_state.web_url = ""
if "web_folder" not in st.session_state:
    st.session_state.web_folder = ""

# --- PURGE LOGIC ---
def purge_website_state():
    """Cleans up all downstream session states when a new URL is fetched."""
    keys_to_delete = ["enhanced_text", "quiz_state", "web_edit_area"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

# --- PAYLOAD GENERATORS ---
def get_website_llm_payload(enhanced=False):
    base = f"Source URL: {st.session_state.web_url}\n\nArticle Text:\n{st.session_state.web_markdown}"
    if enhanced and st.session_state.get('enhanced_text'):
        return f"{base}\n\nCurrent Notes:\n{st.session_state.enhanced_text}"
    return base

def get_website_quiz_payload():
    if st.session_state.get('enhanced_text'):
        return f"Generate a quiz based on these notes:\n{st.session_state.enhanced_text}"
    return f"Generate a quiz based on this article:\n{st.session_state.web_markdown}"


# ==========================================
# UI LAYOUT
# ==========================================

with st.sidebar:
    st.title("🌐 Website Processor")
    st.markdown("Paste an article URL below to extract its content, review it side-by-side, and process it.")

    # --- INGESTION FORM ---
    with st.form("url_fetch_form"):
        target_url = st.text_input("Enter Article URL:")
        fetch_button = st.form_submit_button("Fetch Website", type="primary")
        
        if fetch_button and target_url:
            with st.spinner("Scraping and processing..."):
                result = scrape_website_to_markdown(BASE_WEB_DIR, target_url)
                
                if result["error"]:
                    st.error(result["error"])
                else:
                    if target_url != st.session_state.web_url:
                        purge_website_state()
                    
                    st.session_state.web_url = target_url
                    st.session_state.web_markdown = result["markdown"]
                    st.session_state.web_folder = result["folder"]
                    
                    st.success("Website extracted successfully!")
                    st.rerun()

    st.divider()

# --- SIDE-BY-SIDE VIEW & EDITOR ---
if st.session_state.web_markdown:
    
    # Create the two columns, matching your PDF page layout
    col_web, col_text = st.columns([1, 1])
    
    # LEFT COLUMN: Live Website View
    with col_web:
        st.subheader("Source Website")
        # Add the candid disclaimer about iframe blocking
        st.caption("⚠️ *Note: Some websites block embedding for security reasons. If the box below is blank or shows an error, the extraction still worked, but the site refuses to display here.*")
        
        # Streamlit's native component for iframes. 
        # Scrolling=True ensures long articles can be read.
        components.iframe(st.session_state.web_url, height=800, scrolling=True)

    # RIGHT COLUMN: Extracted Markdown & Editing
    with col_text:
        st.subheader("Extracted Markdown")
        
        # 1. PREVIEW TOGGLE
        # Exactly the same logic you used in the PDF script
        is_preview_mode = st.toggle("👁️ Preview Formatting Mode", value=False)
        
        # 2. SAVE EDITS FUNCTION
        def save_web_edits():
            """Updates session state AND saves manual edits back to the local .md cache."""
            # Update the state with what's in the text box
            st.session_state.web_markdown = st.session_state.web_edit_area
            
            # Reconstruct the file path and save it so cache stays fresh
            url_hash = get_url_hash(st.session_state.web_url)
            md_path = os.path.join(st.session_state.web_folder, f"{url_hash}.md")
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(st.session_state.web_markdown)
                
        # 3. CONDITIONAL RENDERING (Preview vs Editor)
        if is_preview_mode:
            # Show rendered markdown inside a fixed-height box so it matches the iframe height
            with st.container(height=800, border=True):
                st.markdown(st.session_state.web_markdown, unsafe_allow_html=True)
        else:
            # Show the raw text area tied to the on_change callback
            st.text_area(
                "Edit Markdown", 
                value=st.session_state.web_markdown, 
                height=800, 
                key="web_edit_area", 
                on_change=save_web_edits,
                label_visibility="collapsed"
            )

    st.divider()
    
    # --- DOWNSTREAM PIPELINE (Shared UI) ---
    render_enhancement_step(
        doc_id=st.session_state.web_url,
        doc_title="Web Article", 
        manager=ai_manager, 
        get_payload_func=get_website_llm_payload,  
        default_prompt="Web_Article_Summary", 
        default_temp=0.7,                     
        default_tokens=8000,
        CACHE_DIR=st.session_state.web_folder 
    )
    
    render_quiz_step(
        doc_id=st.session_state.web_url, 
        manager=ai_manager, 
        get_quiz_payload_func=get_website_quiz_payload,
        CACHE_DIR=st.session_state.web_folder
    )