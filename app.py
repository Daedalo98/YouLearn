import os
import json
import streamlit as st
from dotenv import load_dotenv
from streamlit_player import st_player
import functions
import AI_manager as manager
import threading  
import time

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

# quiz-related states
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []  # Holds the parsed JSON questions
if "liked_questions" not in st.session_state:
    st.session_state.liked_questions = {} # Tracks Y/N for each question
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = "setup"  # setup, waiting, answering, reviewing, finished
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "current_q" not in st.session_state:
    st.session_state.current_q = {}
if "q_count" not in st.session_state:
    st.session_state.q_count = 1
if "question_queue" not in st.session_state:
    st.session_state.question_queue = [] # Standard python list for cross-thread sharing
if "bg_thread_status" not in st.session_state:
    st.session_state.bg_thread_status = {"running": False} # Dictionary allows pass-by-reference

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
                    # check if enhanced transcript already exists on disk and, if so, load it instead of regenerating (this allows persistence across sessions and also prevents data loss if the user forgets to save edits before generating)
                    cached_path = os.path.join(CACHE_DIR, f"{st.session_state.video_id}_enhanced.md")
                    if os.path.exists(cached_path):
                        with open(cached_path, "r", encoding="utf-8") as f:
                            st.session_state.enhanced_text = f.read()

                    else:
                        # Formats metadata and transcript for the LLM
                        llm_payload = functions.prepare_llm_payload(enhanced=False)
                        
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

                    # save the generated text to a .md file in the cache directory for easy retrieval
                    output_path = os.path.join(CACHE_DIR, f"{st.session_state.video_id}_enhanced.md")
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(st.session_state.enhanced_text)

            # regenerate with notes: if the user has already generated once, they may have made edits in the text area. We want to use those edits as the new source of truth for the LLM input to allow iterative refinement without losing changes.
            if st.button("🔄 Regenerate with Notes", use_container_width=True):
                if not st.session_state.enhanced_text:
                    st.warning("No existing enhanced text found. Please generate a note first.")
                else:
                    llm_payload = functions.prepare_llm_payload(enhanced=True)
                    
                    st.session_state.enhanced_text = ""
                    text_placeholder = st.empty()
                    
                    if streaming_on:
                        full_text = ""
                        with st.status(f"Regenerating with notes using {text_model}...", expanded=True) as status:
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
                        # actually save the file
                        output_path = os.path.join(CACHE_DIR, f"{st.session_state.video_id}_enhanced.md")
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(st.session_state.enhanced_text)
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
    # STEP 3: ADAPTIVE BATCHED QUIZ ENGINE
    # ==========================================
    st.divider()
    st.header("🧠 Step 3: Adaptive Quiz")
    
    with st.container(border=True):
        col_q_prompt, col_q_output = st.columns([1, 2])
        
        # --- LEFT COLUMN: SETTINGS ---
        with col_q_prompt:
            st.subheader("Quiz Parameters")
            
            is_unlimited = st.checkbox("Unlimited Questions", value=False)
            target_questions = 999 if is_unlimited else st.number_input("Target Number of Questions", 1, 100, 10, disabled=is_unlimited)
            num_options = st.number_input("Options per Question", 2, 6, 4)
            batch_quiz = st.number_input("Batch Generation Size", 1, 10, 4, help="How many questions the LLM generates in the background at once.")
            
            st.divider()
            st.subheader("LLM Settings")
            with st.expander("🧠 Active Models & Gen Options", expanded=False):
                available_models = manager.get_models()
                default_models = ["No models found"] if not available_models else available_models
                text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0
                text_model_quiz = st.selectbox("Text Generation Model", default_models, index=text_idx, key="quiz_text_model")
                temperature_quiz = st.number_input("Temperature", 0.0, 2.0, 0.3, 0.1, key="quiz_temp")
                max_tokens_quiz = st.number_input("Max Tokens", 100, 5000, 2000, 100, key="quiz_tokens")

            prompts_dict = functions.load_prompts(PROMPTS_FILE)
            quiz_prompt_name = st.selectbox("Active Prompt", list(prompts_dict.keys()), index=list(prompts_dict.keys()).index("Quiz_Generator") if "Quiz_Generator" in prompts_dict else 0, key="quiz_prompt_sel")
            quiz_system_prompt = st.text_area("Edit Current Prompt", prompts_dict[quiz_prompt_name], height=150, key="quiz_prompt_area")
            
            if st.session_state.quiz_state != "setup":
                if st.button("🔄 Reset Quiz", use_container_width=True):
                    st.session_state.quiz_state = "setup"
                    st.session_state.quiz_history = []
                    st.session_state.question_queue = []
                    st.session_state.current_q = {}
                    st.session_state.q_count = 1
                    st.rerun()

        # --- RIGHT COLUMN: ACTIVE FLASHCARD ---
        with col_q_output:
            st.subheader("Interactive Flashcard")
            
            if not st.session_state.get("enhanced_text", "").strip():
                st.caption("*Generate your Enhanced Output in Step 2 to unlock the quiz engine.*")
            else:
                # ==========================================
                # THREAD CONTROLLER & DASHBOARD
                # ==========================================
                # Trigger a new batch generation if the queue falls below the batch size
                if st.session_state.quiz_state not in ["setup", "finished"]:
                    if len(st.session_state.question_queue) < batch_quiz and not st.session_state.bg_thread_status.get("running"):
                        threading.Thread(
                            target=functions.bg_fetch_batch, # (or functions.bg_fetch_batch)
                            args=(
                                st.session_state.question_queue,
                                st.session_state.bg_thread_status,
                                functions.prepare_quiz_payload(),
                                st.session_state.quiz_history,
                                quiz_system_prompt,
                                text_model_quiz,
                                temperature_quiz,
                                max_tokens_quiz,
                                num_options,
                                batch_quiz,
                                manager
                            )
                        ).start()

                # --- DASHBOARD ---
                if st.session_state.quiz_state not in ["setup", "finished"]:
                    dash_col1, dash_col2 = st.columns(2)
                    with dash_col1:
                        st.caption(f"**Ready in Queue:** {len(st.session_state.question_queue)} questions")
                    with dash_col2:
                        if st.session_state.bg_thread_status.get("running"):
                            st.caption("⚙️ **Worker:** 🟢 Generating Batch...")
                        else:
                            st.caption("⚙️ **Worker:** 💤 Idle")
                            
                    if st.session_state.bg_thread_status.get("error"):
                        st.error(f"⚠️ Background Error: {st.session_state.bg_thread_status['error']}")
                        
                    with st.expander("🔍 View Active Prompt Payload"):
                        st.text(st.session_state.bg_thread_status.get("last_payload", "No payload generated yet."))
                st.divider()
                # ==========================================

                # 1. SETUP STATE
                if st.session_state.quiz_state == "setup":
                    st.info(f"Target: {'Unlimited' if is_unlimited else target_questions} Questions | Options: {num_options} | Batching: {batch_quiz}")
                    if st.button("🚀 Start Adaptive Quiz", type="primary", use_container_width=True):
                        st.session_state.quiz_state = "waiting"
                        st.rerun()

                # 2. WAITING STATE
                elif st.session_state.quiz_state == "waiting":
                    if len(st.session_state.question_queue) > 0:
                        st.session_state.current_q = st.session_state.question_queue.pop(0)
                        st.session_state.quiz_state = "answering"
                        st.rerun()
                    else:
                        with st.spinner(f"Generating your first batch of {batch_quiz} questions..."):
                            time.sleep(1)
                            st.rerun()

                # 3. ANSWERING STATE
                elif st.session_state.quiz_state == "answering":
                    q_data = st.session_state.current_q
                    st.markdown(f"### Question {st.session_state.q_count}")
                    st.markdown(f"**{q_data.get('question', 'Error loading question.')}**")
                    
                    opts = q_data.get('options', []) + ["I don't know"]
                    user_choice = st.radio("Select an answer:", opts, key=f"radio_q_{st.session_state.q_count}")
                    
                    if st.button("Submit Answer", type="primary"):
                        st.session_state.quiz_state = "reviewing"
                        st.session_state.current_q['user_choice'] = user_choice
                        # Evaluate and save status for the context builder
                        is_correct = functions.check_answer(user_choice, q_data.get('answer', ''))
                        st.session_state.current_q['is_correct'] = is_correct
                        st.rerun()

                # 4. REVIEWING STATE
                elif st.session_state.quiz_state == "reviewing":
                    q_data = st.session_state.current_q
                    st.markdown(f"### Question {st.session_state.q_count}")
                    st.markdown(f"**{q_data.get('question')}**")
                    
                    correct_answer = q_data.get('answer', '')
                    user_answer = q_data.get('user_choice', '')
                    is_correct = q_data.get('is_correct', False)
                    
                    if user_answer == "I don't know":
                        st.warning("You skipped this one! That's okay, active recall takes practice.")
                        st.success(f"**The Correct Answer was:** {correct_answer}")
                    elif is_correct:
                        st.success(f"**Correct!** You chose: {user_answer}")
                    else:
                        st.error(f"**Incorrect.** You chose: {user_answer}")
                        st.success(f"**Correct Answer:** {correct_answer}")
                        
                    st.info(f"**Explanation:** {q_data.get('explanation', 'No explanation provided.')}")
                    
                    st.divider()
                    # THE LIKING PARAMETER (0 to 100)
                    like_score = st.slider("Rate the quality of this question (0 = Useless, 100 = Great)", 0, 100, 50, key=f"like_slider_{st.session_state.q_count}")
                    
                    # Next Step Logic
                    if not is_unlimited and st.session_state.q_count >= target_questions:
                        if st.button("🎉 Finish Quiz", type="primary", use_container_width=True):
                            st.session_state.current_q['like_score'] = like_score
                            st.session_state.quiz_state = "finished"
                            st.session_state.quiz_history.append(st.session_state.current_q)
                            st.rerun()
                    else:
                        btn_label = "Next Question ⚡" if len(st.session_state.question_queue) > 0 else "Next Question ⏳"
                        if st.button(btn_label, type="primary", use_container_width=True):
                            st.session_state.current_q['like_score'] = like_score
                            st.session_state.quiz_state = "waiting"
                            st.session_state.quiz_history.append(st.session_state.current_q)
                            st.session_state.q_count += 1
                            st.rerun()

                # 5. FINISHED STATE
                elif st.session_state.quiz_state == "finished":
                    st.success("### Quiz Complete!")
                    st.write(f"You answered {len(st.session_state.quiz_history)} questions.")
                    correct_count = sum(1 for q in st.session_state.quiz_history if q.get('is_correct', False))
                    st.metric("Final Score", f"{correct_count} / {len(st.session_state.quiz_history)}")
                    
                    # Show top rated questions
                    st.subheader("Your Top Rated Questions")
                    best_qs = sorted(st.session_state.quiz_history, key=lambda x: x.get('like_score', 0), reverse=True)
                    for q in best_qs[:5]: # Show top 5
                        if q.get('like_score', 0) > 50:
                            st.markdown(f"- **{q.get('question')}** (Score: {q.get('like_score')})")



else:
    st.info("👈 Enter a YouTube URL in the sidebar and click 'Fetch' to begin.")

