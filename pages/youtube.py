import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_player import st_player
import functions
import AI_manager as manager
import spreader
import json

# Load environment variables from the .env file
# load_dotenv()

# ==========================================
# PAGE CONFIGURATION & SETUP
# ==========================================
st.set_page_config(layout="wide", page_title="YouTube Transcript Sync", page_icon="🎥")

# Create a local directory for caching transcripts
if "CACHE_DIR" not in st.session_state:
    st.session_state.CACHE_DIR = "saved_transcripts"
    if not os.path.exists(st.session_state.CACHE_DIR):
        os.makedirs(st.session_state.CACHE_DIR)
        
if "PROMPTS_FILE" not in st.session_state:
    st.session_state.PROMPTS_FILE = "system_prompts.json"

# INSTEAD: Initialize the manager securely in session state
if "manager" not in st.session_state:
    st.session_state.manager = manager.Manager(
        gemini_api_key=st.session_state.get("gemini_key", ""),
        openai_api_key=st.session_state.get("openai_key", "")
    )

if "prompts_dict" not in st.session_state:
    # Default prompts loaded into memory on first run
    st.session_state.prompts_dict = {
        "Obsidian_Default": "You are an expert knowledge manager. Process the provided metadata and transcript into a highly structured, Obsidian-style Markdown note to enhance the comprehension of the provided text.\n\nCRITICAL INSTRUCTION for appropriate formatting of the answer:\n0. Include a title at the top using the video title (# video title).\n1. Include a YAML frontmatter block with: tags (e.g., #tag1, #tag2), aliases, author, date, and source url.\n2. Create a brief 'Summary' section.\n3. Create a 'Key Insights' section using bullet points.\n4. Format the main concepts under clear header sections.\n5. Include a 'Related / Connections' section at the bottom for internal wiki linking (e.g., [[Concept Name]]).\n6. Do NOT hallucinate. Rely strictly on the provided transcript.\n\nCONSTRAINTS:\n- NEVER hallucinate.\n- make sure that EVERY key information of the text is transposed.\n- analyze in depth and help comprehension.\n- follow CRITICAL INSTRUCTION for appropriate formatting of the answer.\n- detail and define pivotal points using info from the provided text.",
        "Questions_Generator": "You are an adaptive expert educator. Based on the provided notes, generate questions.\n Ensure each question is different from previous ones.\n You MUST output ONLY a valid JSON object. No markdown, no arrays, no conversational text.\n",
        "Answers_Generator": "You are an adaptive expert educator. Based on the provided notes and questions, generate answers.\n Ensure each answer is different from previous ones and only one and only one answer must be the correct answer.\n You MUST output ONLY a valid JSON object. No markdown, no arrays, no conversational text.\n",
        "RAG_query": "You are an expert search query optimizer for a Retrieval-Augmented Generation (RAG) system.\n Your goal is to take a user's raw brain-dump and expand it to maximize its semantic footprint for a vector database search over academic/technical Markdown files.\n Instructions:\n 1. Identify the core concepts in the raw query.\n 2. Add relevant synonyms, related technical terms, and broader/narrower concepts.\n 3. Formulate the output as a comprehensive, prolix paragraph. Do NOT use bullet points. \n 4. Do NOT attempt to answer the query. Only expand the search terms.\n 5. Do NOT include any preamble or postscript. The output should be a single, standalone paragraph ready for embedding and searching.\n\n CRITICAL INSTRUCTION: The output MUST be a single, comprehensive paragraph that expands the original query with related concepts and synonyms. Do NOT use bullet points or lists. Do NOT include any preamble or postscript.",
        "Academic_generator": "You are an expert academic researcher and writer. Your task is to synthesize the provided context blocks to comprehensively and objectively answer the user's query.\n Adhere STRICTLY to the following rules:\n 1. ABSOLUTE GROUNDING: Rely exclusively on the provided context. Do not introduce outside knowledge, and absolutely do not hallucinate facts or data. If the context does not contain enough information to fully answer the query, explicitly state the limitations of the provided text.\n 2. ACADEMIC SYNTHESIS: Do not simply summarize each source sequentially. Integrate the information cohesively, grouping by themes, arguments, or chronological developments. Maintain a formal, objective, and scholarly tone.\n 3. NO REFERENCE LIST: DO NOT generate a 'References,' 'Bibliography,' or 'Works Cited' section at the end of your response. DO NOT use [...] to address to names or numbers.\n4. IN-TEXT ATTRIBUTION: When making a specific claim, use the knowledge of the retrieved chunks, but DO NOT attribute it to the relevant source using the provided source names (e.g., \"As noted in [Source Name]...\" or \"...(Source Name).\").\nThe system pipeline will automatically append verified citations programmatically, so you DO NOT.",
        
        "YouTube_Summary": """You are a rigid data-extraction script. Your ONLY function is to map the provided text into the exact Markdown template below.

        <CRITICAL_RULES>
        1. NO PREAMBLE. NO POSTSCRIPT. Do NOT say 'Here is the note' or 'Sure!'.
        2. The very first character of your output MUST be the '#' symbol.
        3. Wrap all key domain terminology in double brackets for Obsidian linking (e.g., [[Machine Learning]]).
        4. Use bullet points extensively. Do NOT write long paragraphs, BUT be exhaustive.
        </CRITICAL_RULES>

        <TEMPLATE>
        # {TITLE}

        ## 🎯 Core Thesis
        > [Insert a 3-4 sentence summary of the primary argument or finding here.]

        ## 🔑 Key Concepts & Definitions
        * **[[Concept 1]]**: [Definition based on text]
        * **[[Concept 2]]**: [Definition based on text]

        ## 🛠️ Methodology / Approach
        * [Bullet point detailing step 1 of their approach]
        * [Bullet point detailing step 2]

        ## 📊 Primary Results & Findings
        * [Key finding 1]
        * [Key finding 2]

        ## 🧠 Conclusions & Implications
        * [Conclusion 1]
        * [Conclusion 2]
        </TEMPLATE>

        BEGIN EXACT TEMPLATE OUTPUT NOW:"""
        }
    
# ==========================================
# SYSTEM LOGGER INITIALIZATION
# ==========================================
import datetime

if "app_logs" not in st.session_state:
    st.session_state.app_logs = []

def add_log(message: str):
    """Appends a timestamped log to the session state."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.app_logs.insert(0, f"[{timestamp}] {message}")


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
    
# ==========================================
# UI LAYOUT & INTERACTION
# ==========================================

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
# USER SETTINGS & CREDENTIALS
# ==========================================
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Changed to "Optional" so users know they can skip this if using Ollama
    with st.expander("Cloud API Keys (Optional)", expanded=True): 
        
        user_gemini_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_key", ""))
        user_openai_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("openai_key", ""))
        
        # We removed the Cache Directory and Prompts File inputs entirely!

        if st.button("Save Keys", width="stretch"):
            # 1. Save keys to session state
            st.session_state.gemini_key = user_gemini_key
            st.session_state.openai_key = user_openai_key
            
            # 2. Re-initialize the manager so it picks up the new keys immediately
            st.session_state.manager = manager.Manager(
                gemini_api_key=st.session_state.gemini_key,
                openai_api_key=st.session_state.openai_key
            )
            st.success("Keys applied! Cloud models unlocked.")

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
                add_log(f"User requested extraction for URL: {input_url}")
                
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
                    # Removed CACHE_DIR argument!
                    full_data_dict = functions.fetch_transcript_with_logs(input_url, video_id)
                    
                    if full_data_dict and full_data_dict.get("segments"):
                        st.session_state.transcript = full_data_dict["segments"]
                        st.session_state.metadata = full_data_dict.get("metadata", {}) 
                        st.session_state.start_time = 0.0
                        
                        add_log(f"Successfully loaded transcript for {video_id}.")
                        status.update(label="Transcript Ready!", state="complete", expanded=False)
                        
                        # ONLY RERUN IF SUCCESSFUL!
                        st.rerun() 
                    else:
                        add_log(f"Failed to fetch data for {video_id}.")
                        status.update(label="Failed to fetch valid data. Read logs above.", state="error", expanded=True)
                        # NO RERUN HERE. Let the user read the error message.
            else:
                st.warning("Please enter a valid YouTube URL first.")

    st.divider()

    # ---------------------------------------------------------
    # OPTION 2: LOAD SAVED VIDEO
    # ---------------------------------------------------------

    st.subheader("Load Saved Workspace")
    uploaded_file = st.file_uploader("Upload a previously downloaded .json file", type=["json"])

    if uploaded_file is not None:
        if st.button("📁 Load Data from File", use_container_width=True):
            try:
                # Read the JSON file the user just uploaded
                loaded_data = json.load(uploaded_file)
                
                # Populate session state
                st.session_state.transcript = loaded_data.get("segments", [])
                st.session_state.metadata = loaded_data.get("metadata", {})
                st.session_state.video_id = loaded_data.get("video_id", "")
                st.session_state.video_url = loaded_data.get("metadata", {}).get("video_url", "")
                st.session_state.enhanced_text = loaded_data.get("enhanced_text", "")
                
                st.toast("Data successfully loaded from file!", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load file. It might be corrupted. Error: {e}")

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

    # ---------------------------------------------------------    
    # Export Workspace
    # ---------------------------------------------------------

    st.subheader("💾 Export Current Workspace")
    # Check if there is actual data to export
    if st.session_state.get("transcript"):
        
        # Bundle the data they need to restore the session
        export_dict = {
            "video_id": st.session_state.video_id,
            "metadata": st.session_state.metadata,
            "segments": st.session_state.transcript,
            "enhanced_text": st.session_state.enhanced_text
        }
        
        # Convert dict to a formatted JSON string
        json_string = json.dumps(export_dict, indent=4)
        
        st.download_button(
            label="📥 Download Session as JSON",
            data=json_string,
            file_name=f"transcript_data_{st.session_state.video_id}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.info("No active video to export.")

    # ---------------------------------------------------------
    # System Logs
    # ---------------------------------------------------------
    st.divider()
    st.subheader("📝 System Logs")
    with st.container(height=300, border=True):
        if not st.session_state.app_logs:
            st.caption("No logs yet...")
        else:
            for log in st.session_state.app_logs:
                st.text(log) # st.text keeps the formatting clean

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
            if st.button(f"⏱️ {timestamp_str}", key=unique_btn_key, width='stretch'):
                st.session_state.start_time = start_sec
                st.rerun()
        
        with text_col:
            # 🚨 THE FIX: The callback must grab the exact unique key
            def update_text(index=i, key_name=unique_txt_key):
                # Update the main memory with the new text
                st.session_state.transcript[index]['text'] = st.session_state[key_name]
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


# ==========================================
# STEP 2: LLM-BASED SUMMARIZATION
# ==========================================

st.header("✨ Step 2: Summarization via LLM")

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
            available_models = st.session_state.manager.get_models()
            default_models = ["No models found"] if not available_models else available_models
            text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0

            text_model = st.selectbox("Text Generation Model", default_models, index=text_idx, key="enh_model")
            st.divider()

            temperature = st.number_input("Temperature", 0.0, 2.0, DEFAULT_TEMP, 0.1)
            max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 10000, DEFAULT_TOKENS, 100)
            streaming_on = st.toggle("Streaming Generation", value=True)

        # -----------------------
        # system prompt selection
        # -----------------------

        st.subheader("System Prompts")
        
        # 1. Get available prompts and determine the default index
        prompt_names = list(st.session_state.prompts_dict.keys())
        default_idx = prompt_names.index(DEFAULT_PROMPT) if DEFAULT_PROMPT in prompt_names else 0
        
        # 2. Render the Selectbox (No complex callbacks needed anymore!)
        selected_prompt_name = st.selectbox(
            "Active Prompt", 
            prompt_names, 
            index=default_idx
        )
        
        # 3. Grab the actual text from the dictionary based on the selection
        current_prompt_text = st.session_state.prompts_dict.get(selected_prompt_name, "")
        
        # 4. Render Text Area using a DYNAMIC KEY. 
        # Why this works: By putting the name of the prompt in the key, Streamlit 
        # treats it as a brand new text area every time you change the dropdown, 
        # forcing it to load the correct `current_prompt_text` value!
        system_prompt = st.text_area(
            "Edit Current Prompt", 
            value=current_prompt_text, 
            height=200, 
            key=f"prompt_box_{selected_prompt_name}" 
        )
        
        # 5. Save Logic
        with st.expander("Save / Modify Prompt"):
            new_prompt_name = st.text_input("Save as (Prompt Name)", value=selected_prompt_name)
            
            if st.button("Save Prompt to Session", width='stretch'):
                if new_prompt_name and system_prompt:
                    # Update the dictionary in memory
                    st.session_state.prompts_dict[new_prompt_name] = system_prompt
                    st.success("Prompt saved to current session!")
                    st.rerun()

    # UI Rendering based on memory state
    if st.session_state.enhanced_text:
        st.info("📝 A generated note already exists for this document.")
        
        # Modern Streamlit popup to prevent accidental overwrites
        with st.popover("⚠️ Recreate Note", width='stretch'):
            st.markdown("This will **permanently overwrite** your existing Markdown note and any manual edits. Are you sure?")
            if st.button("Yes, Overwrite Note", type="primary", width='stretch'):
                # Pass None for the cached_path, your functions.py should be updated 
                # to return the text instead of writing to a file!
                new_text = functions.run_generation(
                    st.session_state.manager, 
                    llm_payload, 
                    system_prompt, 
                    text_model, 
                    temperature, 
                    max_tokens, 
                    streaming_on
                )
                if new_text:
                    st.session_state.enhanced_text = new_text
                st.rerun()
    else:
        if st.button("🚀 Generate Note", width='stretch', type="primary"):
            new_text = functions.run_generation(
                st.session_state.manager, 
                llm_payload, 
                system_prompt, 
                text_model, 
                temperature, 
                max_tokens, 
                streaming_on
            )
            if new_text:
                st.session_state.enhanced_text = new_text
            st.rerun()

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
                    with open(os.path.join(st.session_state.CACHE_DIR, f"{st.session_state.video_id}_enhanced.md"), "w", encoding="utf-8") as f:
                        f.write(st.session_state.enhanced_text)
                    st.rerun()
            else:
                st.markdown(st.session_state.enhanced_text)
                
            st.download_button("📥 Download Note as .md", st.session_state.enhanced_text, f"{st.session_state.video_id}.md", "text/markdown", width='stretch')



# ==========================================
# SPREADER MODULE INJECTION
# ==========================================
# We pass the 'enhanced_text' from session state into the spreader.
# It will only show up as an expander.
st.markdown("---") # Add a nice visual divider
st.header("Spreader")

# Safely get enhanced text. If it doesn't exist yet, pass an empty string.
current_enhanced_text = st.session_state.get("enhanced_text", "")
spreader.render_spreader_module(current_enhanced_text) # <-- 2. INJECT HERE


# ==========================================
# STEP 3: METACOGNITIVE QUIZ 
# ==========================================

from shared_ui import render_quiz_step

def get_quiz_payload():
    if st.session_state.get('enhanced_text'):
        return st.session_state.enhanced_text
    else:
        st.warning("No enhanced text available yet. Using original transcript for quiz generation.")
        return st.session_state.transcript

st.markdown("---") # Add a nice visual divider
st.header("📝 Step 3: Metacognitive Quiz Generation")
load_quiz = st.button("Generate Quiz from Enhanced Note", type="primary", use_container_width=True)

if load_quiz:
    if not st.session_state.get('enhanced_text'):
        st.warning("No enhanced text available yet. Using original transcript for quiz generation.")
    st.session_state.quiz_state = "setup"
    st.rerun()

if st.session_state.get('quiz_state') == "setup": 
    render_quiz_step(
        doc_id=st.session_state.video_id, 
        manager=st.session_state.manager, 
        get_quiz_payload_func=get_quiz_payload
    )