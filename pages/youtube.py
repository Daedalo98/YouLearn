import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_player import st_player
import functions
import AI_manager as manager
from shared_ui import render_enhancement_step, render_quiz_step, get_quiz_payload
import spreader

# Callbacks for YouTube payload generation
def yt_get_llm_payload(enhanced=False):
    return functions.prepare_llm_payload(enhanced)

def yt_get_quiz_payload():
    return functions.prepare_quiz_payload()

# Load environment variables from the .env file
load_dotenv()

# ==========================================
# 1. PAGE CONFIGURATION & SETUP
# ==========================================
st.set_page_config(layout="wide", page_title="YouTube Transcript Sync", page_icon="🎥")

# Create a local directory for caching transcripts
CACHE_DIR = "saved_transcripts"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

PROMPTS_FILE = "system_prompts.json"

@st.cache_resource
def get_manager(): return manager.Manager()
manager = get_manager()

# ==========================================
# 2. MODULAR FUNCTIONS (Business Logic)
# ==========================================

## moved into functions.py for better organization


# ==========================================
# 3. STATE INITIALIZATION
# ==========================================

if "transcript" not in st.session_state:
    st.session_state.transcript = []
if "video_url" not in st.session_state:
    st.session_state.video_url = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "metadata" not in st.session_state:
    st.session_state.metadata = {}
if "video_id" not in st.session_state:
    st.session_state.video_id = ""
if "enhanced_text" not in st.session_state:
    st.session_state.enhanced_text = ""
if "is_editing_enhanced" not in st.session_state:
    st.session_state.is_editing_enhanced = False

# zoom related states
if "global_zoom" not in st.session_state:
    st.session_state.global_zoom = 16

def sync_zoom(slider_key):
    """Callback to update the global zoom whenever ANY of the local sliders are moved."""
    st.session_state.global_zoom = st.session_state[slider_key]

# quiz-related states
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = "setup" # setup, q_gen, evaluating, answering, finished
if "q_list" not in st.session_state:
    st.session_state.q_list = [] # Raw strings from Qmodel
if "evaluations" not in st.session_state:
    st.session_state.evaluations = {} # Stores user confidence and liking
if "a_model_data" not in st.session_state:
    st.session_state.a_model_data = [] # Stores the final Amodel output
if "bg_thread_status" not in st.session_state:
    st.session_state.bg_thread_status = {"running": False, "done": False, "result": None, "error": None}
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0.0
if "regenerated_indices" not in st.session_state:
    st.session_state.regenerated_indices = set()

# ==========================================
# 4. UI LAYOUT & INTERACTION
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    input_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Fetch & Process Transcript", type="primary"):
        if input_url.strip():  
            video_id = functions.extract_video_id(input_url)
            st.session_state.video_url = input_url
            st.session_state.video_id = video_id
            
            with st.status("Processing Request...", expanded=True) as status:
                full_data_dict = functions.fetch_transcript_with_logs(CACHE_DIR, input_url, video_id)
                if full_data_dict and full_data_dict.get("segments"):
                    st.session_state.transcript = full_data_dict["segments"]
                    st.session_state.metadata = full_data_dict.get("metadata", {}) 
                    st.session_state.start_time = 0.0
                    status.update(label="Transcript Ready!", state="complete", expanded=False)
                else:
                    status.update(label="Failed to fetch valid data.", state="error", expanded=True)
        else:
            st.warning("Please enter a valid YouTube URL first.")
        # reload the page for the new video data to take effect
        st.rerun()
        # clear step 2 and 3
        st.session_state.enhanced_text = ""
        

    # Sidebar Video & Controls
    if st.session_state.video_id and st.session_state.transcript:
        st.divider()
        st.subheader("Video Playback")
        
        # We construct a privacy-enhanced embed URL
        nocookie_url = f"https://www.youtube-nocookie.com/embed/{st.session_state.video_id}"
        
        st_player(
            nocookie_url,
            # Switched autoplay to 0 so we stop spamming YouTube's servers on every rerun
            config={"playerVars": {"start": int(float(st.session_state.start_time)), "autoplay": 0}},
            key=f"player_{st.session_state.start_time}"
        )

# --- Main Layout ---
st.title("🎬 YouTube Transcript Editor")
st.header("Step 1: Review & Edit Transcript")

# ==========================================
# MAGIC CSS INJECTION (Globally Scaled)
# ==========================================
st.markdown(f"""
    <style>
        .stTextArea textarea {{ font-size: {st.session_state.global_zoom}px !important; line-height: 1.5 !important; }}
        .stMarkdown p, .stMarkdown li {{ font-size: {st.session_state.global_zoom}px !important; line-height: 1.5 !important; }}
        .stRadio p, .stCheckbox p, .stAlert p {{ font-size: {st.session_state.global_zoom}px !important; line-height: 1.5 !important; }}
    </style>
""", unsafe_allow_html=True)
# ==========================================

#if st.session_state.video_url and st.session_state.transcript:

# Display Video Info
if "metadata" in st.session_state and st.session_state.metadata:
    meta = st.session_state.metadata
    st.markdown(f"### 📺 {meta.get('title', 'Unknown Title')}")
    st.caption(f"**Channel:** {meta.get('author_name', 'Unknown')} | **Uploaded:** {meta.get('upload_date', 'Unknown')} | **Source:** [Link]({meta.get('video_url', '')})")
    st.divider()

# --- NEW: Global Read/Edit Toggle & Zoom Control ---
st.markdown("**Markdown Supported:** Use `**bold**`, `*italic*`, `# Heading`, or `<u>underline</u>`")

# We put the toggle and the zoom slider side-by-side
ctrl_col1, ctrl_col2 = st.columns([1, 1])
with ctrl_col1:
    is_preview_mode = st.toggle("👁️ Preview Formatting Mode", value=False)
with ctrl_col2:
    # Slider controls the font size from 10px up to a massive 50px
    with ctrl_col2:
        st.slider("🔍 Zoom Text Size (px)", min_value=10, max_value=50, value=st.session_state.global_zoom, key="zoom_step1", on_change=sync_zoom, args=("zoom_step1",), label_visibility="collapsed")
        
transcript_container = st.container(height=600)

with transcript_container:
    for i, segment in enumerate(st.session_state.transcript):
        
        # Failsafe: Ensure segment is actually a dictionary
        if not isinstance(segment, dict):
            continue
            
        start_sec = segment.get('start', 0.0)
        timestamp_str = functions.format_timestamp(start_sec)
        current_text = str(segment.get('text', '')) # Force as string
        
        # Simple 2-column layout for each row
        # adaptively adjust column widths based on content (e.g., if timestamp is long, give it more space)
        # Calculate dynamic column widths based on text length
        text_length = len(current_text)
        btn_ratio = 0.15 if text_length < 100 else 0.12
        text_ratio = 1 - btn_ratio
        btn_col, text_col = st.columns([btn_ratio, text_ratio])
        
        with btn_col:
            if st.button(f"⏱️ {timestamp_str}", key=f"btn_{i}", use_container_width=True):
                st.session_state.start_time = start_sec
                st.rerun()
        
        with text_col:
            def update_text(index=i):
                st.session_state.transcript[index]['text'] = st.session_state[f"text_{index}"]
                functions.save_edits_to_disk(CACHE_DIR)
                st.toast("💾 Auto-saved!", icon="✅")

            # If the toggle is ON, render the beautiful formatted text
            if is_preview_mode:
                # Use a markdown block to render sizes, bold, italic, etc.
                st.markdown(current_text, unsafe_allow_html=True)
            
            # If the toggle is OFF, show the raw editor
            else:
                st.text_area(
                    "Edit Text", 
                    value=current_text, 
                    key=f"text_{i}", 
                    label_visibility="collapsed",
                    height=100,
                    on_change=update_text
                )

        
        st.markdown("<hr style='margin: 0.2em 0px; border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)
        
# Render exactly like we did in PDF
render_enhancement_step(
    doc_id=st.session_state.video_id, 
    doc_title=st.session_state.metadata.get('title', 'Untitled Video'),
    manager=manager, 
    get_payload_func=yt_get_llm_payload,  
    default_prompt="Obsidian_Academic_Note", 
    default_temp=0.7,                     
    default_tokens=8000,
    CACHE_DIR = "saved_transcripts"
)


# ==========================================
# NEW: SPREADER MODULE INJECTION
# ==========================================
# We pass the 'enhanced_text' from session state into the spreader.
# It will only show up as an expander.
st.markdown("---") # Add a nice visual divider
st.header("Spreader")

# Safely get enhanced text. If it doesn't exist yet, pass an empty string.
current_enhanced_text = st.session_state.get("enhanced_text", "")
spreader.render_spreader_module(current_enhanced_text) # <-- 2. INJECT HERE

# ==========================================


render_quiz_step(
    doc_id=st.session_state.video_id,
    manager=manager,
    get_quiz_payload_func=get_quiz_payload,
    CACHE_DIR = "saved_transcripts"
)