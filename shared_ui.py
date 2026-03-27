import streamlit as st
import os
import re
import json
import threading
import time
import functions

# Define constants
CACHE_DIR = "saved_transcripts"
PROMPTS_FILE = "system_prompts.json"

def init_shared_state():
    """Ensures all shared variables exist in the session state."""
    if "enhanced_text" not in st.session_state:
        st.session_state.enhanced_text = ""
    if "is_editing_enhanced" not in st.session_state:
        st.session_state.is_editing_enhanced = False
    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = "setup"
    if "q_list" not in st.session_state:
        st.session_state.q_list = []
    if "evaluations" not in st.session_state:
        st.session_state.evaluations = {}
    if "a_model_data" not in st.session_state:
        st.session_state.a_model_data = []
    if "bg_thread_status" not in st.session_state:
        st.session_state.bg_thread_status = {"running": False, "done": False, "result": None, "error": None}
    if "regenerated_indices" not in st.session_state:
        st.session_state.regenerated_indices = set()
    if "global_zoom" not in st.session_state:
        st.session_state.global_zoom = 16

def sync_zoom(slider_key):
    st.session_state.global_zoom = st.session_state[slider_key]

def render_enhancement_step(
    doc_id: str, 
    doc_title: str, 
    manager, 
    get_payload_func, 
    default_prompt: str,
    default_temp: float,                       
    default_tokens: int                       
    ):

    """
    Renders Step 2: LLM Enhancement
    - doc_id: Unique ID for saving the file (e.g., video_id or DOI)
    - doc_title: Used for the download button
    - manager: AI_manager instance
    - get_payload_func: A callback function `func(enhanced: bool)` returning the text for the LLM
    """

    init_shared_state()
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

                text_model = st.selectbox("Text Generation Model", default_models, index=text_idx, key="enh_model")
                st.divider()

                temperature = st.number_input("Temperature", 0.0, 2.0, default_temp, 0.1)
                max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 10000, default_tokens, 100)
                streaming_on = st.toggle("Streaming Generation", value=True)

            st.subheader("System Prompts")
            prompts_dict = functions.load_prompts(PROMPTS_FILE)
            prompt_names = list(prompts_dict.keys())
            
            # Determine default index
            default_idx = prompt_names.index(default_prompt) if default_prompt in prompt_names else 0
            
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

            # GENERATE LOGIC
            cached_path = os.path.join(CACHE_DIR, f"{doc_id}_enhanced.md")
            file_exists = os.path.exists(cached_path)

            # Helper function to avoid duplicating the generation code
            def run_generation():
                llm_payload = get_payload_func(enhanced=False) 
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
                    with st.status(f"Generating Output...", expanded=True) as status:
                        st.session_state.enhanced_text = manager.generate_sync(llm_payload, system_prompt, text_model, temperature, max_tokens)
                        status.update(label="Complete!", state="complete", expanded=False)

                # Save the new text to disk
                with open(cached_path, "w", encoding="utf-8") as f:
                    f.write(st.session_state.enhanced_text)

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
                            run_generation()
                            st.rerun() # Refresh UI to show the new text
            else:
                if st.button("🚀 Generate Note", use_container_width=True, type="primary"):
                    run_generation()

        with col_output:
            st.subheader("Enhanced Output (.md)")
            st.slider("🔍 Zoom Text Size", min_value=10, max_value=50, value=st.session_state.global_zoom, key="zoom_step2", on_change=sync_zoom, args=("zoom_step2",))
            
            if st.session_state.enhanced_text:
                mode_enh = st.toggle("✏️ Edit Markdown Mode", value=st.session_state.is_editing_enhanced)
                st.session_state.is_editing_enhanced = mode_enh
                
                if st.session_state.is_editing_enhanced:
                    edited = st.text_area("Edit Final Note", st.session_state.enhanced_text, height=600, label_visibility="collapsed")
                    if st.button("Save Markdown Edits", type="primary"):
                        st.session_state.enhanced_text = edited
                        st.toast("Edits saved!", icon="✅")
                        st.session_state.is_editing_enhanced = False
                        with open(os.path.join(CACHE_DIR, f"{doc_id}_enhanced.md"), "w", encoding="utf-8") as f:
                            f.write(st.session_state.enhanced_text)
                        st.rerun()
                else:
                    st.markdown(st.session_state.enhanced_text)
                    
                st.download_button("📥 Download Note as .md", st.session_state.enhanced_text, f"{doc_title}.md", "text/markdown", use_container_width=True)

def render_quiz_step(doc_id: str, manager, get_quiz_payload_func):
    """
    Renders Step 3: Metacognitive Exam.
    Takes `get_quiz_payload_func()` to grab text dynamically.
    (NOTE: Your exact Q-model / A-model logic goes here. I am keeping it identical.)
    """
    init_shared_state()
    st.divider()
    st.header("🧠 Step 3: Metacognitive Exam")
    
    with st.container(border=True):
        col_q_prompt, col_q_output = st.columns([1, 2])
        
        # --- LEFT COLUMN: SETTINGS ---
        with col_q_prompt:
            st.subheader("Quiz Parameters")
            quiz_n = st.number_input("Total Questions (N)", 1, 50, 5)
            num_options = st.number_input("Options per Question", 2, 6, 4)

            with st.expander("⚖️ Scoring Multipliers"):
                mult_sure = st.number_input("Certainty Multiplier", 0.0, 5.0, 1.0, 0.1)
                mult_doubt = st.number_input("Doubt Multiplier", 0.0, 5.0, 1.0, 0.1)
                mult_idk = st.number_input("Ignorance Multiplier", 0.0, 5.0, 1.0, 0.1)
            
            st.divider()
            st.subheader("LLM Architecture Settings")
            
            available_models = manager.get_models()
            default_models = ["No models found"] if not available_models else available_models
            text_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0
            prompts_dict = functions.load_prompts(PROMPTS_FILE)
            questions_prompt_idx = list(prompts_dict.keys()).index("Questions_Generator") if "Questions_Generator" in prompts_dict else 0
            answers_prompt_idx = list(prompts_dict.keys()).index("Answers_Generator") if "Answers_Generator" in prompts_dict else 0
                        
            # TABS FOR INDEPENDENT MODEL CONTROL
            tab_q, tab_a = st.tabs(["🗣️ Q-Model (Ideation)", "📝 A-Model (Answers)"])
            
            with tab_q:
                q_model = st.selectbox("Q-Model Selection", default_models, index=text_idx, key="q_mod")
                q_temp = st.number_input("Temperature", 0.0, 2.0, 0.5, 0.1, key="q_temp", help="Higher = more creative questions.")
                q_tok = st.number_input("Max Tokens", 100, 5000, 1000, 100, key="q_tok")
                q_stream = st.toggle("Stream Output", value=True, key="q_stream")
                
                q_prompt_name = st.selectbox("System Prompt", list(prompts_dict.keys()), index=questions_prompt_idx, key="q_prompt_sel")
                q_sys_prompt = st.text_area("Edit Q-Model Prompt", prompts_dict[q_prompt_name], height=150, key="q_prompt_area")
            
            with tab_a:
                a_model = st.selectbox("A-Model Selection", default_models, index=text_idx, key="a_mod")
                a_temp = st.number_input("Temperature", 0.0, 2.0, 0.2, 0.1, key="a_temp", help="Lower = stricter JSON adherence.")
                a_tok = st.number_input("Max Tokens", 100, 5000, 2000, 100, key="a_tok")
                # A-Model runs in background, so streaming is forced off for UI stability
                st.caption("*A-Model runs synchronously in the background.*")
                
                a_prompt_name = st.selectbox("System Prompt", list(prompts_dict.keys()), index=answers_prompt_idx, key="a_prompt_sel")
                a_sys_prompt = st.text_area("Edit A-Model Prompt", prompts_dict[a_prompt_name], height=150, key="a_prompt_area")
            
            st.divider()
            if st.session_state.quiz_state != "setup":
                if st.button("🔄 Reset Exam Engine", use_container_width=True):
                    st.session_state.quiz_state = "setup"
                    st.session_state.q_list = []
                    st.session_state.evaluations = {}
                    st.session_state.a_model_data = []
                    st.session_state.bg_thread_status = {"running": False, "done": False, "result": None, "error": None}
                    st.session_state.quiz_score = 0.0
                    st.session_state.q_payload_log = ""
                    st.rerun()


        # --- RIGHT COLUMN: WORKFLOW ---
        with col_q_output:
            st.subheader("Interactive Exam")
            
            # Global Zoom Slider for Quiz
            st.slider("🔍 Zoom Text Size", min_value=10, max_value=50, value=st.session_state.global_zoom, key="zoom_step3", on_change=sync_zoom, args=("zoom_step3",), label_visibility="collapsed")
            
            if not st.session_state.get("enhanced_text", "").strip():
                st.caption("*Generate your Enhanced Output in Step 2 to unlock the exam engine.*")
            else:
                
                # 1. SETUP STATE
                if st.session_state.quiz_state == "setup":
                    st.info(f"Engine Ready: {quiz_n} Questions.")
                    if st.button("🚀 Generate Exam Concepts (Q-Model)", type="primary", use_container_width=True):
                        st.session_state.quiz_state = "q_gen"
                        st.rerun()

                # 2. Q-GEN STATE (With Active Stream Interceptor)
                elif st.session_state.quiz_state == "q_gen":
                    llm_payload = functions.prepare_quiz_payload()
                    
                    q_dynamic_prompt = (
                        f"{q_sys_prompt}\n\n"
                        f"CRITICAL INSTRUCTION: Generate EXACTLY {quiz_n} different questions based on this text.\n"
                        f"You MUST output ONLY a plain JSON list of strings.\n"
                        f"Format strictly like this: [\"Question 1?\", \"Question 2?\"]\n"
                    )
                    
                    st.session_state.q_payload_log = f"--- Q-MODEL SYSTEM PROMPT ---\n{q_dynamic_prompt}\n\n--- DOCUMENT PAYLOAD ---\n{llm_payload}"
                    
                    with st.status(f"Q-Model brainstorming {quiz_n} questions...", expanded=True) as status:
                        q_output = ""
                        matches = []
                        
                        if q_stream:
                            stream_ph = st.empty()
                            for chunk in manager.generate_stream(llm_payload, q_dynamic_prompt, q_model, q_temp, q_tok):
                                q_output += chunk
                                stream_ph.markdown(f"```json\n{q_output}▌\n```")
                                
                                # THE STREAM INTERCEPTOR
                                # Continuously check how many valid strings we have in the raw output
                                matches = re.findall(r'"(.*?)"', q_output)
                                if len(matches) >= quiz_n:
                                    st.toast("Target reached! Intercepting stream early.", icon="⚡")
                                    break # Kills the LLM generation instantly!
                                    
                            stream_ph.empty()
                        else:
                            q_output = manager.generate_sync(llm_payload, q_dynamic_prompt, q_model, q_temp, q_tok)
                            matches = re.findall(r'"(.*?)"', q_output)
                        
                        # Proceed with exactly N matches
                        if len(matches) >= quiz_n:
                            st.session_state.q_list = matches[:quiz_n] 
                            st.session_state.regenerated_indices = set() # Reset tracker
                            status.update(label="Questions Generated!", state="complete", expanded=False)
                            st.session_state.quiz_state = "evaluating"
                            st.rerun()
                        else:
                            status.update(label="Failed to generate enough questions.", state="error", expanded=True)
                            st.error(f"Raw Output: {q_output}")
                            if st.button("Retry"): st.rerun()

                # 3. EVALUATING STATE (With Live Regeneration)
                elif st.session_state.quiz_state == "evaluating":
                    with st.expander("🔍 View Q-Model Payload"):
                        st.text(st.session_state.get("q_payload_log", ""))
                        
                    # Kick off background A-Model using the ORIGINAL list
                    if not st.session_state.bg_thread_status["running"] and not st.session_state.bg_thread_status["done"]:
                        threading.Thread(
                            target=functions.bg_fetch_answers, 
                            args=(
                                st.session_state.bg_thread_status,
                                functions.prepare_quiz_payload(),
                                st.session_state.q_list,
                                a_sys_prompt,
                                a_model,
                                a_temp,
                                a_tok,
                                num_options,
                                manager
                            )
                        ).start()
                    
                    st.info("🧠 **Metacognitive Phase:** Rate your confidence. You can regenerate questions you don't like.")
                    
                    if st.session_state.bg_thread_status["running"]:
                        st.caption("⚙️ *A-Model is generating options in the background...*")
                    elif st.session_state.bg_thread_status["done"]:
                        st.caption("✅ *A-Model background task complete!*")

                    # Live UI (Not inside a form, so buttons work independently!)
                    for i, q_text in enumerate(st.session_state.q_list):
                        col_q, col_btn = st.columns([8, 1])
                        with col_q:
                            st.markdown(f"**Q{i+1}: {q_text}**")

                        st.radio("Confidence:", ["I am SURE", "I am NOT SURE", "I DON'T KNOW"], key=f"conf_{i}", horizontal=True)
                        st.slider("Liking Score (0=Useless, 5=Great)", 0, 5, 3, key=f"like_{i}")
                        st.divider()
                    
                    if st.button("Submit Evaluations & Proceed", type="primary", use_container_width=True):
                        for i in range(len(st.session_state.q_list)):
                            st.session_state.evaluations[i] = {
                                "confidence": st.session_state[f"conf_{i}"],
                                "liking": st.session_state[f"like_{i}"]
                            }
                        st.session_state.quiz_state = "a_wait"
                        st.rerun()

                # 4. A-WAIT STATE (With A-Model Patching)
                elif st.session_state.quiz_state == "a_wait":
                    if st.session_state.bg_thread_status["done"]:
                        if st.session_state.bg_thread_status["error"]:
                            st.error(f"A-Model Error: {st.session_state.bg_thread_status['error']}")
                        else:
                            raw_a_data = st.session_state.bg_thread_status["result"]
                            
                            # THE PATCH JOB: If you swapped questions, we need to fix their answers!
                            if st.session_state.regenerated_indices:
                                with st.spinner(f"Patching answers for {len(st.session_state.regenerated_indices)} swapped questions..."):
                                    questions_to_patch = [st.session_state.q_list[i] for i in st.session_state.regenerated_indices]
                                    llm_payload = functions.prepare_quiz_payload()
                                    patch_prompt = (
                                        f"{a_sys_prompt}\n\n"
                                        f"Build a multiple-choice quiz for EXACTLY these {len(questions_to_patch)} questions:\n"
                                        f"{json.dumps(questions_to_patch)}\n"
                                        f"Each MUST have exactly {num_options} options. Return a JSON array."
                                    )
                                    patch_out = manager.generate_sync(llm_payload, patch_prompt, a_model, a_temp, a_tok)
                                    
                                    start_p = patch_out.find('[')
                                    end_p = patch_out.rfind(']')
                                    if start_p != -1 and end_p != -1:
                                        patch_data = json.loads(patch_out[start_p:end_p+1])
                                        patch_data = [{str(k).lower().strip(): v for k, v in q.items()} for q in patch_data]
                                        
                                        # Inject the patched answers back into the raw data in the correct spots
                                        patch_idx = 0
                                        for orig_idx in sorted(list(st.session_state.regenerated_indices)):
                                            raw_a_data[orig_idx] = patch_data[patch_idx]
                                            patch_idx += 1

                            st.session_state.a_model_data = []
                            for i, item in enumerate(raw_a_data):
                                item["eval_conf"] = st.session_state.evaluations[i]["confidence"]
                                item["eval_like"] = st.session_state.evaluations[i]["liking"]
                                st.session_state.a_model_data.append(item)
                                
                            st.session_state.quiz_state = "taking_quiz"
                            st.rerun()
                    else:
                        with st.spinner("A-Model is finishing the background generation..."):
                            time.sleep(1)
                            st.rerun()

                # 5. TAKING EXAM STATE (All questions visible)
                elif st.session_state.quiz_state == "taking_quiz":
                    with st.expander("🔍 View A-Model Payload"):
                        st.text(st.session_state.bg_thread_status.get("last_payload", ""))
                        
                    st.info("📜 **Full Exam:** Scroll to review all questions. Change answers as needed.")
                    
                    with st.form("exam_form"):
                        for idx, q_data in enumerate(st.session_state.a_model_data):
                            st.markdown(f"### Q{idx+1}: {q_data.get('question')}")
                            st.caption(f"*Your Confidence: {q_data['eval_conf']}*")
                            
                            opts = q_data.get('options', []) + ["I don't know"]
                            st.radio("Options", opts, key=f"user_ans_{idx}", label_visibility="collapsed")
                            st.markdown("<hr style='margin: 1em 0px; border-top: 1px dashed #bbb;'>", unsafe_allow_html=True)
                            
                        if st.form_submit_button("Submit Final Answers", type="primary", use_container_width=True):
                            # Save all answers from the form directly into memory
                            for idx in range(len(st.session_state.a_model_data)):
                                st.session_state.a_model_data[idx]['user_choice'] = st.session_state[f"user_ans_{idx}"]
                            st.session_state.quiz_state = "reviewing"
                            st.rerun()

                # 6. REVIEWING STATE (Results & Scoring)
                elif st.session_state.quiz_state == "reviewing":
                    st.success("### Exam Complete!")
                    
                    total_score = 0.0
                    
                    # Display all questions and results
                    for idx, q_data in enumerate(st.session_state.a_model_data):
                        st.markdown(f"### Q{idx+1}: {q_data.get('question')}")
                        
                        c_ans = q_data.get('answer', '')
                        u_ans = q_data.get('user_choice', '')
                        is_correct = functions.check_answer(u_ans, c_ans) 
                        
                        points = 0.0
                        if is_correct:
                            if q_data['eval_conf'] == "I am SURE": points = mult_sure
                            elif q_data['eval_conf'] == "I am NOT SURE": points = mult_doubt
                            elif q_data['eval_conf'] == "I DON'T KNOW": points = mult_idk
                            st.success(f"**Correct!** (+{points} pts) You chose: {u_ans}")
                        else:
                            if u_ans == "I don't know":
                                st.warning("Skipped.")
                            else:
                                st.error(f"**Incorrect.** You chose: {u_ans}")
                            st.success(f"**Correct Answer:** {c_ans}")
                            
                        total_score += points
                        st.info(f"**Explanation:** {q_data.get('explanation', '')}")
                        
                        # Flag Checkbox for each question
                        q_data['flagged'] = st.checkbox("🚩 Flag as Incorrect/Inappropriate", key=f"flag_{idx}")
                        st.markdown("<hr style='margin: 1em 0px; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
                        
                    st.metric("Weighted Final Score", f"{total_score:.2f}")
                    
                    if st.button("💾 Append Valid Questions to Notes (.md)", type="primary"):
                        append_text = "\n\n---\n## 🧠 Active Recall Questions\n\n"
                        saved_count = 0
                        for q in st.session_state.a_model_data:
                            if q.get('flagged', False): continue
                            if q.get('eval_like', 0) < 3: continue
                            append_text += f"**{q.get('question')}** *(Liking: {q.get('eval_like')}/5)* \n\n"
                            saved_count += 1
                            
                        st.session_state.enhanced_text += append_text
                        st.success(f"Successfully appended {saved_count} questions to your Markdown note in Step 2!")
                        # save the new file
                        output_path = os.path.join(CACHE_DIR, f"{st.session_state.video_id}_enhanced.md")
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(st.session_state.enhanced_text)
                        st.rerun()
                        # once appended, disabilitate button
                        st.session_state.quiz_state = "finalized"
