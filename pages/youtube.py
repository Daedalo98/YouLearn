import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_player import st_player
from functions import llm_settings, run_generation
import functions
import AI_manager as manager
import spreader

# Load environment variables from the .env file
load_dotenv()

# ==========================================
# PAGE CONFIGURATION & SETUP
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
# STATE INITIALIZATION
# ==========================================

if "transcript" not in st.session_state:
    st.session_state.transcript = []
if "video_url" not in st.session_state:
    st.session_state.video_url = ""
if "video_id" not in st.session_state:
    st.session_state.video_id = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "metadata" not in st.session_state:
    st.session_state.metadata = {}
if "enhanced_text" not in st.session_state:
    st.session_state.enhanced_text = ""
if "is_editing_enhanced" not in st.session_state:
    st.session_state.is_editing_enhanced = False
    
# zoom related states
if "global_zoom" not in st.session_state:
    st.session_state.global_zoom = 22 # Default font size in pixels

def sync_zoom(slider_key):
    """Callback to update the global zoom whenever ANY of the local sliders are moved."""
    for slider in ["zoom_step1", "zoom_step2"]:
        if slider != slider_key:
            st.session_state[slider] = st.session_state[slider_key]
            st.session_state.global_zoom = st.session_state[slider_key]

# ==========================================
# UI LAYOUT & INTERACTION
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")

    # ---------------------------------------------------------
    # OPTION 1: INGEST NEW VIDEO
    # ---------------------------------------------------------
    st.subheader("Ingest New Video")
    with st.form("fetch_transcript_form"):
        input_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        submit_btn = st.form_submit_button("Fetch & Process Transcript", type="primary")
    
    if submit_btn:
        if input_url.strip():  
            video_id = functions.extract_video_id(input_url)
            st.toast(f"Processing ID: {video_id}", icon="🔍")
            
            # --- PURGE OLD STATE ---
            st.session_state.transcript = []
            st.session_state.metadata = {}
            st.session_state.video_url = ""
            st.session_state.video_id = ""
            st.session_state.enhanced_text = ""
            st.session_state.quiz_state = "setup"
            
            for key in list(st.session_state.keys()):
                if key.startswith("text_") or key.startswith("btn_"):
                    del st.session_state[key]
            
            # --- FETCH NEW DATA ---
            st.session_state.video_url = input_url
            st.session_state.video_id = video_id
            
            with st.status(f"Processing Request for {video_id}...", expanded=True) as status:
                full_data_dict = functions.fetch_transcript_with_logs(CACHE_DIR, input_url, video_id)
                
                if full_data_dict and full_data_dict.get("segments"):
                    st.session_state.transcript = full_data_dict["segments"]
                    st.session_state.metadata = full_data_dict.get("metadata", {}) 
                    st.session_state.start_time = 0.0
                    status.update(label="Transcript Ready!", state="complete", expanded=False)
                else:
                    status.update(label="Failed to fetch valid data. Check API/URL.", state="error", expanded=True)
            
            st.rerun()
        else:
            st.warning("Please enter a valid YouTube URL first.")

    st.divider()

    # ---------------------------------------------------------
    # OPTION 2: LOAD SAVED VIDEO
    # ---------------------------------------------------------
    st.subheader("Load Saved Video")
    
    # 1. Scan the directory to get our available files
    cached_videos = functions.get_cached_videos(CACHE_DIR)
    
    if not cached_videos:
        st.info("No saved videos found. Fetch a new URL above to get started!")
    else:
        # 2. Create a dropdown list. 
        # `options` gets the list of IDs (the keys).
        # `format_func` tells Streamlit to display the Title (the value) in the UI instead of the ID.
        video_id = st.selectbox(
            "Select a previous video:",
            options=list(cached_videos.keys()),
            format_func=lambda x: cached_videos[x]
        )
        
        # 3. Handle the Load logic
        if st.button("📁 Load Video", use_container_width=True):
            
            # --- PURGE OLD STATE (Exactly like the new fetch) ---
            st.session_state.transcript = []
            st.session_state.metadata = {}
            st.session_state.video_url = ""
            st.session_state.video_id = ""
            st.session_state.enhanced_text = ""
            st.session_state.quiz_state = "setup"
            
            for key in list(st.session_state.keys()):
                if key.startswith("text_") or key.startswith("btn_"):
                    del st.session_state[key]
                    
            # --- LOAD DATA FROM DISK ---
            loaded_data = functions.load_cached_video(CACHE_DIR, video_id)
            
            if loaded_data and "segments" in loaded_data:
                # Inject the local data into memory
                st.session_state.transcript = loaded_data["segments"]
                st.session_state.metadata = loaded_data.get("metadata", {})
                st.session_state.video_id = video_id
                st.session_state.video_url = loaded_data.get("metadata", {}).get("video_url", f"https://youtube.com/watch?v={video_id}")
                st.session_state.start_time = 0.0
                
                st.toast(f"Successfully loaded '{cached_videos[video_id]}'!", icon="✅")
                st.rerun()
            else:
                st.error("Failed to load the local file. It might be corrupted.")
        
    # ---------------------------------------------------------
    # VIDEO PLAYBACK (Shared by both logic paths)
    # ---------------------------------------------------------
    if st.session_state.video_id and st.session_state.transcript:
        st.divider()
        st.subheader("Video Playback")
        
        nocookie_url = f"https://www.youtube-nocookie.com/embed/{st.session_state.video_id}"
        
        st_player(
            nocookie_url,
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

# Display Video Info
if "metadata" in st.session_state and st.session_state.metadata:
    st.info(f"**Diagnostic Check:** Current Video ID in memory is `{st.session_state.video_id}`")
    meta = st.session_state.metadata
    st.markdown(f"### 📺 {meta.get('title', 'Unknown Title')}")
    st.caption(f"**Channel:** {meta.get('author_name', 'Unknown')} | **Uploaded:** {meta.get('upload_date', 'Unknown')} | **Source:** [Link]({meta.get('video_url', '')})")
    st.divider()

# --- NEW: Global Read/Edit Toggle & Zoom Control ---
st.markdown("**Markdown Supported:** Use `**bold**`, `*italic*`, `# Heading`, or `<u>underline</u>`")

ctrl_col1, ctrl_col2 = st.columns([1, 1])
with ctrl_col1:
    st.markdown("<p style='text-align: right;'>Text Size:</p>", unsafe_allow_html=True)
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
        
        text_length = len(current_text)
        btn_ratio = 0.15 if text_length < 100 else 0.12
        text_ratio = 1 - btn_ratio
        btn_col, text_col = st.columns([btn_ratio, text_ratio])
        
        # 🚨 THE FIX: Create globally unique keys tied to THIS specific video
        unique_btn_key = f"btn_{st.session_state.video_id}_{i}"
        unique_txt_key = f"text_{st.session_state.video_id}_{i}"
        
        with btn_col:
            if st.button(f"⏱️ {timestamp_str}", key=unique_btn_key, use_container_width=True):
                st.session_state.start_time = start_sec
                st.rerun()
        
        with text_col:
            # 🚨 THE FIX: The callback must grab the exact unique key
            def update_text(index=i, key_name=unique_txt_key):
                # Update the main memory with the new text
                st.session_state.transcript[index]['text'] = st.session_state[key_name]
                functions.save_edits_to_disk(CACHE_DIR)
                st.toast("💾 Auto-saved!", icon="✅")

            st.text_area(
                "Edit Text", 
                value=current_text, 
                key=unique_txt_key,  # Applies the unique key here!
                label_visibility="collapsed",
                height=100,
                on_change=update_text
            )
        
        st.markdown("<hr style='margin: 0.2em 0px; border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)

st.header("✨ Step 2: Summarization via LLM")

cached_path = os.path.join(CACHE_DIR, f"{video_id}_enhanced.md")
file_exists = os.path.exists(cached_path)

meta = st.session_state.metadata

# Extract just the text from the segment dictionaries
text_only = "\n".join([seg.get("text", "") for seg in st.session_state.transcript])

llm_payload = (
    f"--- METADATA ---\n"
    f"Title: {meta.get('title', 'Unknown')}\n"
    f"Author: {meta.get('author_name', 'Unknown')}\n"
    f"Date: {meta.get('upload_date', 'Unknown')}\n"
    f"URL: {meta.get('video_url', 'Unknown')}\n\n"
    f"--- REDACTED TRANSCRIPT ---\n"
    f"{text_only}"
)

DEFAULT_TEMP = 0.5
DEFAULT_TOKENS = 10000
DEFAULT_PROMPT = "YouTube_Summary"

ctrl_col1, ctrl_col2 = st.columns([1, 1])
with ctrl_col1:
    st.markdown("<p style='text-align: right;'>Text Size:</p>", unsafe_allow_html=True)
with ctrl_col2:
    # Slider controls the font size from 10px up to a massive 50px
    with ctrl_col2:
        st.slider("🔍 Zoom Text Size (px)", min_value=10, max_value=50, value=st.session_state.global_zoom, key="zoom_step2", on_change=sync_zoom, args=("zoom_step2",), label_visibility="collapsed")
        
with st.container(border=True):
    col_prompt, col_output = st.columns([1, 2])
    
    with col_prompt:
        st.subheader("LLM Settings")
        with st.expander("🧠 Active Models & Gen Options", expanded=True):
            available_models = manager.get_models()
            default_models = ["No models found"] if not available_models else available_models
            text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0

            text_model = st.selectbox("Text Generation Model", default_models, index=text_idx, key="enh_model")
            st.divider()

            temperature = st.number_input("Temperature", 0.0, 2.0, DEFAULT_TEMP, 0.1)
            max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 10000, DEFAULT_TOKENS, 100)
            streaming_on = st.toggle("Streaming Generation", value=True)

        st.subheader("System Prompts")
        prompts_dict = functions.load_prompts(PROMPTS_FILE)
        prompt_names = list(prompts_dict.keys())
        
        # Determine default index
        default_idx = prompt_names.index(DEFAULT_PROMPT) if DEFAULT_PROMPT in prompt_names else 0
        
        # 1. INITIALIZE STATE FIRST
        # We must set this before the widgets render so the default prompt is ready.
        if "text_prompt_area" not in st.session_state:
            st.session_state.text_prompt_area = prompts_dict.get(prompt_names[default_idx], "")

        # 2. DEFINE THE CALLBACK
        def sync_prompt_to_area():
            """Forces the text area state to match the newly selected dropdown item."""
            selected = st.session_state.text_prompt_sel
            st.session_state.text_prompt_area = prompts_dict.get(selected, "")

        # 3. RENDER SELECTBOX AND CAPTURE THE NAME
        selected_prompt_name = st.selectbox(
            "Active Prompt", 
            prompt_names, 
            index=default_idx, 
            key="text_prompt_sel",
            on_change=sync_prompt_to_area
        )
        
        # 4. RENDER TEXT AREA (No 'value' parameter needed, the key handles it)
        system_prompt = st.text_area("Edit Current Prompt", height=200, key="text_prompt_area")
        
        # 5. USE THE SELECTED NAME FOR SAVING (Restoring your original feature)
        with st.expander("Save / Modify Prompt"):
            # Here is where selected_prompt_name is actually used!
            new_prompt_name = st.text_input("Save as (Prompt Name)", value=selected_prompt_name)
            
            if st.button("Save Prompt", use_container_width=True):
                if new_prompt_name and system_prompt:
                    functions.save_prompt(PROMPTS_FILE, new_prompt_name, system_prompt)
                    st.success("Saved!")
                    st.rerun()

    # UI Rendering based on file existence
    if file_exists:
        st.info("📝 A generated note already exists for this document.")
        col_load, col_recreate = st.columns(2)
        
        with col_load:
            if st.button("📂 Load Existing Note", use_container_width=True):
                with open(cached_path, "r", encoding="utf-8") as f:
                    st.session_state.enhanced_text = f.read()
                    
        with col_recreate:
            # Modern Streamlit popup alternative
            with st.popover("⚠️ Recreate Note", use_container_width=True):
                st.markdown("This will **permanently overwrite** your existing Markdown note and any manual edits. Are you sure?")
                if st.button("Yes, Overwrite Note", type="primary", use_container_width=True):
                    functions.run_generation(
                        manager, 
                        llm_payload, 
                        system_prompt, 
                        text_model, 
                        temperature, 
                        max_tokens, 
                        cached_path, 
                        streaming_on
                        )
                    
                    st.rerun() # Refresh UI to show the new text
    else:
        if st.button("🚀 Generate Note", use_container_width=True, type="primary"):
            functions.run_generation(
                manager, 
                llm_payload, 
                system_prompt, 
                text_model, 
                temperature, 
                max_tokens, 
                cached_path, 
                streaming_on
                )

    with col_output:
        st.subheader("Enhanced Output (.md)")

        if st.session_state.enhanced_text:
            mode_enh = st.toggle("✏️ Edit Markdown Mode", value=st.session_state.is_editing_enhanced)
            st.session_state.is_editing_enhanced = mode_enh
            
            if st.session_state.is_editing_enhanced:
                edited = st.text_area("Edit Final Note", st.session_state.enhanced_text, height=600, label_visibility="collapsed")
                if st.button("Save Markdown Edits", type="primary"):
                    st.session_state.enhanced_text = edited
                    st.toast("Edits saved!", icon="✅")
                    st.session_state.is_editing_enhanced = False
                    with open(os.path.join(CACHE_DIR, f"{video_id}_enhanced.md"), "w", encoding="utf-8") as f:
                        f.write(st.session_state.enhanced_text)
                    st.rerun()
            else:
                st.markdown(st.session_state.enhanced_text)
                
            st.download_button("📥 Download Note as .md", st.session_state.enhanced_text, f"{video_id}.md", "text/markdown", use_container_width=True)



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
