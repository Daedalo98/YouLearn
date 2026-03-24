import os
import re
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from streamlit_player import st_player
import functions
import AI_manager as manager

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
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []  # Holds the parsed JSON questions
if "liked_questions" not in st.session_state:
    st.session_state.liked_questions = {} # Tracks Y/N for each question

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

if st.session_state.video_url and st.session_state.transcript:
    
    # Display Video Info
    if "metadata" in st.session_state and st.session_state.metadata:
        meta = st.session_state.metadata
        st.markdown(f"### 📺 {meta.get('title', 'Unknown Title')}")
        st.caption(f"**Channel:** {meta.get('author_name', 'Unknown')} | **Uploaded:** {meta.get('upload_date', 'Unknown')} | **Source:** [Link]({meta.get('video_url', '')})")
        st.divider()
    
    transcript_container = st.container(height=500)
    
    with transcript_container:
        for i, segment in enumerate(st.session_state.transcript):
            
            # Failsafe: Ensure segment is actually a dictionary
            if not isinstance(segment, dict):
                continue
                
            start_sec = segment.get('start', 0.0)
            timestamp_str = functions.format_timestamp(start_sec)
            current_text = str(segment.get('text', '')) # Force as string
            
            # Simple 2-column layout for each row
            btn_col, text_col = st.columns([1.5, 10])
            
            with btn_col:
                if st.button(f"⏱️ {timestamp_str}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.start_time = start_sec
                    st.rerun()
            
            with text_col:
                def update_text(index=i):
                    # 1. Update the memory
                    st.session_state.transcript[index]['text'] = st.session_state[f"text_{index}"]
                    # 2. Save to the JSON file
                    functions.save_edits_to_disk(CACHE_DIR)
                    # 3. Show a tiny temporary success popup in the bottom right corner
                    st.toast("💾 Auto-saved!", icon="✅")

                st.text_area(
                    "Edit Text", 
                    value=current_text, 
                    key=f"text_{i}", 
                    label_visibility="collapsed",
                    height=80,
                    on_change=update_text
                )
            
            st.markdown("<hr style='margin: 0.2em 0px; border-top: 1px dashed #ddd;'>", unsafe_allow_html=True)
            
    # ==========================================
    # STEP 2: LLM ENHANCEMENT
    # ==========================================
    st.divider()
    st.header("✨ Step 2: Enhance via LLM")
    
    with st.container(border=True):
        col_prompt, col_output = st.columns([1, 2])
        
        with col_prompt:
            st.subheader("LLM Settings")
                            
            with st.expander("🧠 Active Models & Gen Options", expanded=True):
                available_models = manager.get_models()
                default_models = ["No models found"] if not available_models else available_models
                text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0
                #embed_idx = default_models.index("gemini-embedding-001") if "gemini-embedding-001" in default_models else 0

                text_model = st.selectbox("Text Generation Model", default_models, index=text_idx)
                #embed_model = st.selectbox("Vector Embedding Model", default_models, index=embed_idx)
                st.divider()
                temperature = st.number_input("Temperature", 0.0, 1000.0, 0.7, 0.1, help="Higher values make output more random")
                max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 10000, 2000, 100)
                streaming_on = st.toggle("Streaming Generation", value=True)

            st.subheader("System Prompts")
            prompts_dict = functions.load_prompts(PROMPTS_FILE)
            selected_prompt_name = st.selectbox("Active Prompt", list(prompts_dict.keys()), index=list(prompts_dict.keys()).index("Obsidian_Note_Generator") if "Obsidian_Note_Generator" in prompts_dict else 0, key="text_prompt_sel")
            system_prompt = st.text_area("Edit Current Prompt", prompts_dict[selected_prompt_name], height=200, key="text_prompt_area")
            
            with st.expander("Save / Modify Prompt"):
                new_prompt_name = st.text_input("Save as (Prompt Name)", value=selected_prompt_name)
                if st.button("Save Prompt", use_container_width=True):
                    if new_prompt_name and system_prompt:
                        functions.save_prompt(PROMPTS_FILE, new_prompt_name, system_prompt)
                        st.success("Saved!")
                        st.rerun()
                        
            if st.button("🚀 Generate Note", use_container_width=True, type="primary"):
                if not st.session_state.transcript:
                    st.warning("Please fetch a transcript in Step 1 first.")
                else:
                    # Formats metadata and transcript for the LLM
                    llm_payload = functions.prepare_llm_payload()
                    
                    st.session_state.enhanced_text = ""
                    text_placeholder = st.empty()
                    
                    if streaming_on:
                        full_text = ""
                        with st.status(f"Generative pass using {text_model}...", expanded=True) as status:
                            for chunk in manager.generate_stream(llm_payload, system_prompt, text_model, temperature, max_tokens):
                                full_text += chunk
                                text_placeholder.markdown(full_text + "▌") 
                            status.update(label="Complete!", state="complete", expanded=False)
                        text_placeholder.empty() 
                        st.session_state.enhanced_text = full_text
                    else:
                        with st.status(f"Generating Output with {text_model}...", expanded=True) as status:
                            full_text = manager.generate_sync(llm_payload, system_prompt, text_model, temperature, max_tokens)
                            status.update(label="Complete!", state="complete", expanded=False)
                            st.session_state.enhanced_text = full_text
                            pass # Placeholder for sync call
                            
        with col_output:
            st.subheader("Enhanced Output (.md)")
            
            if st.session_state.enhanced_text:
                # Toggle between Edit and Read modes for the final note
                mode_enh = st.toggle("✏️ Edit Markdown Mode", value=st.session_state.is_editing_enhanced)
                st.session_state.is_editing_enhanced = mode_enh
                
                if st.session_state.is_editing_enhanced:
                    # We use a button to save to prevent infinite loop typing lag
                    edited = st.text_area("Edit Final Note", st.session_state.enhanced_text, height=600, label_visibility="collapsed")
                    if st.button("Save Markdown Edits", type="primary"):
                        st.session_state.enhanced_text = edited
                        st.toast("Edits saved!", icon="✅")
                        st.session_state.is_editing_enhanced = False
                        st.rerun()
                else:
                    st.markdown(st.session_state.enhanced_text)
                    
                st.divider()
                st.download_button(
                    label="📥 Download Note as .md",
                    data=st.session_state.enhanced_text,
                    file_name=f"{st.session_state.metadata.get('title', 'note')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            else:
                st.caption("*No enhanced text generated yet. Click 'Generate Note' on the left.*")

    # ==========================================
    # STEP 3: QUIZ TIME
    # ==========================================
    st.divider()
    st.header("🧠 Step 3: Quiz Time")
    
    with st.container(border=True):
        col_q_prompt, col_q_output = st.columns([1, 2])
        
        with col_q_prompt:
            st.subheader("LLM Settings")
                            
            with st.expander("🧠 Active Models & Gen Options", expanded=True):
                available_models = manager.get_models()
                default_models = ["No models found"] if not available_models else available_models
                text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0

                # ADDED KEY: "quiz_text_model"
                text_model_quiz = st.selectbox("Text Generation Model", default_models, index=text_idx, key="quiz_text_model")
                
                st.divider()
                
                # ADDED KEYS to inputs to prevent duplicates with Step 2
                temperature_quiz = st.number_input("Temperature", 0.0, 1000.0, 0.7, 0.1, key="quiz_temp", help="Higher values make output more random")
                max_tokens_quiz = st.number_input("Max Tokens (Verbosity)", 100, 10000, 2000, 100, key="quiz_tokens")
                streaming_on_quiz = st.toggle("Streaming Generation", value=True, key="quiz_streaming")

            st.subheader("System Prompts")
            prompts_dict = functions.load_prompts(PROMPTS_FILE)
            
            # These already had unique keys, which is good!
            quiz_prompt_name = st.selectbox("Active Prompt", list(prompts_dict.keys()), index=list(prompts_dict.keys()).index("Quiz_Generator") if "Quiz_Generator" in prompts_dict else 0, key="quiz_prompt_sel")
            quiz_system_prompt = st.text_area("Edit Current Prompt", prompts_dict[quiz_prompt_name], height=150, key="quiz_prompt_area")
            
            # ADDED KEYS to these number inputs
            num_questions = st.number_input("Number of Questions", 1, 100, 5, key="quiz_num_q")
            num_options = st.number_input("Options per Question", 2, 10, 4, key="quiz_num_opt")
            
            with st.expander("Save / Modify Prompt"):
                # FIXED: Added key, and changed value to `quiz_prompt_name` instead of `selected_prompt_name`
                new_prompt_name_quiz = st.text_input("Save as (Prompt Name)", value=quiz_prompt_name, key="quiz_new_prompt_name")
                
                # FIXED: Added key to the button
                if st.button("Save Prompt", use_container_width=True, key="quiz_save_btn"):
                    # FIXED: Now refers to quiz variables instead of Step 2 variables
                    if new_prompt_name_quiz and quiz_system_prompt:
                        functions.save_prompt(PROMPTS_FILE, new_prompt_name_quiz, quiz_system_prompt)
                        st.success("Saved!")
                        st.rerun()
                        
            # Dynamic prompt injection for the parameters
            dynamic_quiz_prompt = f"{quiz_system_prompt}\n\nCRITICAL INSTRUCTION: Generate exactly {num_questions} questions, each with exactly {num_options} options."
            
            if st.button("🎯 Generate Interactive Quiz", use_container_width=True, type="primary"):
                if not st.session_state.transcript:
                    st.warning("Please fetch a transcript in Step 1 first.")
                else:
                    llm_payload = functions.prepare_quiz_payload()

                    st.session_state.enhanced_text = ""
                    text_placeholder = st.empty()
                    
                    if streaming_on_quiz:
                        full_text = ""
                        with st.status(f"Generating Quiz with {text_model_quiz}...", expanded=True) as status:
                            for chunk in manager.generate_stream(llm_payload, quiz_system_prompt, text_model_quiz, temperature_quiz, max_tokens_quiz):
                                full_text += chunk
                                text_placeholder.markdown(full_text + "▌") 
                            status.update(label="Complete!", state="complete", expanded=False)
                        text_placeholder.empty() 
                        st.session_state.enhanced_text = full_text
                    else:
                        with st.status(f"Generating Quiz with {text_model_quiz}...", expanded=True) as status:
                            full_text = manager.generate_sync(llm_payload, quiz_system_prompt, text_model_quiz, temperature_quiz, max_tokens_quiz)
                            status.update(label="Complete!", state="complete", expanded=False)
                            st.session_state.enhanced_text = full_text
                            pass # Placeholder for sync call
                  
                    try:
                        json_match = re.search(r'\[.*\]', full_text, re.DOTALL)
                        if json_match:
                            raw_quiz = json.loads(json_match.group(0))
                            
                            # 3. NORMALIZATION: LLMs love to randomly capitalize keys. 
                            # This forces every key to lowercase (e.g., "Question" -> "question")
                            normalized_quiz = []
                            for item in raw_quiz:
                                norm_item = {str(k).lower(): v for k, v in item.items()}
                                normalized_quiz.append(norm_item)
                            
                            if len(normalized_quiz) > 0:
                                st.session_state.quiz_data = normalized_quiz
                                st.session_state.liked_questions = {i: False for i in range(len(normalized_quiz))}
                                status.update(label=f"Quiz Generated! ({len(normalized_quiz)} questions)", state="complete", expanded=False)
                                
                                # 4. FORCE UI REFRESH: Ensures the right column renders immediately
                                st.rerun() 
                            else:
                                raise ValueError("The LLM returned an empty array `[]`.")
                        else:
                            raise ValueError("No JSON array found in the output.")
                            
                    except Exception as e:
                        status.update(label="Failed to parse quiz format.", state="error", expanded=True)
                        st.error(f"Error parsing JSON: {e}")
                        st.session_state.quiz_data = []
    
else:
    st.info("👈 Enter a YouTube URL in the sidebar and click 'Fetch' to begin.")

