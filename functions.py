import os
import re
import json
import requests
import streamlit as st
import AI_manager as manager

def extract_video_id(url: str) -> str:
    """Extracts the YouTube Video ID from any standard, shortened, live, or shorts URL."""
    # Strip any accidental spaces the user might have copied
    url = url.strip()
    
    # This Regex pattern hunts for the 11-character ID in almost any YouTube URL variation
    regex_pattern = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/|youtube\.com\/live\/)([^\"&?\/\s]{11})"
    
    match = re.search(regex_pattern, url)
    
    if match:
        return match.group(1)
        
    st.error(f"❌ Error: Could not find a valid 11-character video ID in the URL: {url}")
    return ""

def fetch_youtube_metadata(video_url: str) -> dict:
    """Fetches video details via oEmbed and scrapes the HTML for the Upload Date."""
    meta_data = {
        "video_url": video_url, 
        "title": "Unknown Title", 
        "author_name": "Unknown Channel", 
        "author_url": "", 
        "thumbnail_url": "",
        "upload_date": "Unknown Date"
    }
    
    try:
        # 1. Get Title and Author safely from oEmbed
        oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
        resp = requests.get(oembed_url, timeout=5)
        if resp.status_code == 200:
            meta = resp.json()
            meta_data["title"] = meta.get("title", "Unknown Title")
            meta_data["author_name"] = meta.get("author_name", "Unknown Channel")
            meta_data["author_url"] = meta.get("author_url", "")
            meta_data["thumbnail_url"] = meta.get("thumbnail_url", "")
        # 2. Scrape the raw YouTube page for the exact upload date
        html_resp = requests.get(video_url, timeout=5)
        
        # Regex hunts for: <meta itemprop="uploadDate" content="2023-10-25T...">
        date_match = re.search(r'<meta itemprop="uploadDate" content="(.*?)">', html_resp.text)
        if date_match:
            # Split by "T" to just get the YYYY-MM-DD part
            meta_data["upload_date"] = date_match.group(1).split("T")[0] 
            
    except Exception as e:
        st.warning(f"Could not fetch complete metadata: {e}")
    
    return meta_data

def fetch_transcript_with_logs(CACHE_DIR: str, video_url: str, video_id: str) -> dict:
    """Checks local storage first. If not found, fetches API, adds metadata, and saves the full JSON."""
    if not video_id:
        st.error("❌ Could not extract a valid Video ID to use for storage.")
        return {}

    cache_filepath = os.path.join(CACHE_DIR, f"{video_id}.json")

    # --- 1. Check Local Cache (Now expects a dict) ---
    st.write(f"🔍 Checking local storage for `{video_id}.json`...")
    if os.path.exists(cache_filepath):
        try:
            with open(cache_filepath, "r", encoding="utf-8") as f:
                full_data = json.load(f)
            st.success("✅ Full transcript data loaded from local storage!")
            return full_data
        except Exception as e:
            st.error(f"⚠️ Error reading local cache: {e}. Falling back to API.")

    # --- 2. Fetch from API ---
    st.write("🌐 Not found locally. Calling Transcript API...")
    api_key = os.getenv("TRANSCRIPT_API_KEY")
    if not api_key:
        st.error("❌ API Key missing! Please add TRANSCRIPT_API_KEY to your .env file.")
        return {}

    endpoint = "https://transcriptapi.com/api/v2/youtube/transcript"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"video_url": video_url, "format": "json"}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  
        api_data = response.json()
        
        # --- 3. Gather Metadata and Merge ---
        st.write("📊 Fetching Video Metadata...")
        video_metadata = fetch_youtube_metadata(video_url)
        
        # Ensure we have a clean dictionary to save
        full_data = {
            "metadata": video_metadata,
            # Handle different API return structures gracefully
            "segments": api_data.get("segments", api_data.get("transcript", []))
        }
        
        # If API returned a raw list instead of a dict, fix it:
        if not full_data["segments"] and isinstance(api_data, list):
            full_data["segments"] = api_data

        # --- 4. Save to Local Cache ---
        if full_data["segments"]:
            try:
                with open(cache_filepath, "w", encoding="utf-8") as f:
                    # We are now saving the ENTIRE object (Metadata + Segments)
                    json.dump(full_data, f, ensure_ascii=False, indent=4)
                st.write(f"💾 Saved complete data packet to `{cache_filepath}`.")
            except Exception as e:
                st.warning(f"⚠️ Failed to save data locally: {e}")
            
            return full_data
        else:
            st.warning("⚠️ The API returned an empty list of segments.")
            return {}
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API/Network Error: {e}")
        return {}

def format_transcript_for_copy(transcript_data: list) -> str:
    """Compiles the edited transcript segments into a single, clean text block."""
    return "\n\n".join([segment.get('text', '') for segment in transcript_data])

def format_timestamp(seconds) -> str:
    """Helper function to format seconds into MM:SS format."""
    try:
        sec_float = float(seconds)
        mins = int(sec_float // 60)
        secs = int(sec_float % 60)
        return f"{mins:02d}:{secs:02d}"
    except (ValueError, TypeError):
        return "00:00"
    
def save_edits_to_disk(CACHE_DIR: str):
    """Saves the current session state transcript back to the local JSON file."""
    if not st.session_state.get("video_id"):
        return

    cache_filepath = os.path.join(CACHE_DIR, f"{st.session_state.video_id}.json")
    
    # Reconstruct the full data dictionary
    full_data = {
        "metadata": st.session_state.metadata,
        "segments": st.session_state.transcript
    }
    
    try:
        with open(cache_filepath, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"⚠️ Failed to save changes: {e}")

def load_prompts(filepath: str) -> dict:
    """Loads system prompts. Creates default Obsidian and Quiz prompts if missing."""
    default_obsidian = (
        "You are an expert knowledge manager. Process the provided YouTube video metadata and transcript into a highly structured, Obsidian-style Markdown note.\n\n"
        "Requirements:\n"
        "0. Include a title at the top using the video title (# video title).\n"
        "1. Include a YAML frontmatter block with: tags (e.g., #tag1, #tag2), aliases, author, date, and source url.\n"
        "2. Create a brief 'Summary' section.\n"
        "3. Create a 'Key Insights' section using bullet points.\n"
        "4. Format the main concepts under clear header sections.\n"
        "5. Include a 'Related / Connections' section at the bottom for internal wiki linking (e.g., [[Concept Name]]).\n"
        "6. Do NOT hallucinate. Rely strictly on the provided transcript."
    )
    
    default_quiz = (
        "You are an adaptive expert educator. Based on the provided notes and the history of previous questions, generate EXACTLY ONE new multiple-choice question.\n"
        "Ensure the question is different from previous ones. If the user got previous questions wrong, focus on those concepts.\n"
        "You MUST output ONLY a valid JSON object. No markdown, no arrays, no conversational text.\n"
        "Format strictly like this:\n"
        "{\n"
        "  \"question\": \"What is the main topic?\",\n"
        "  \"options\": [\"A\", \"B\", \"C\", \"D\"],\n"
        "  \"answer\": \"A\",\n"
        "  \"explanation\": \"Because the notes state...\"\n"
        "}"
    )

    default_dict = {"Obsidian_Default": default_obsidian, "Quiz_Generator": default_quiz}
    
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                prompts = json.load(f)
                # Merge missing defaults into the loaded prompts
                for k, v in default_dict.items():
                    if k not in prompts:
                        prompts[k] = v
                        save_prompt(filepath, k, v)
                return prompts
        except Exception:
            pass
            
    # If no file exists, create one with both defaults
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(default_dict, f, indent=4)
    return default_dict

def save_prompt(filepath: str, name: str, prompt_text: str):
    """Saves a new or updated prompt to the JSON file."""
    prompts = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            prompts = json.load(f)
    prompts[name] = prompt_text
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=4)

def prepare_llm_payload(enhanced: bool) -> str:
    """Combines metadata and edited transcript into a single string for the LLM."""
    meta = st.session_state.metadata
    
    # Extract just the text from the segment dictionaries
    text_only = "\n".join([seg.get("text", "") for seg in st.session_state.transcript])
    
    payload = (
        f"--- METADATA ---\n"
        f"Title: {meta.get('title', 'Unknown')}\n"
        f"Author: {meta.get('author_name', 'Unknown')}\n"
        f"Date: {meta.get('upload_date', 'Unknown')}\n"
        f"URL: {meta.get('video_url', 'Unknown')}\n\n"
        f"--- REDACTED TRANSCRIPT ---\n"
        f"{text_only}"
    )
    if enhanced:
        payload = (f"--- METADATA ---\n"
                   f"Title: {meta.get('title', 'Unknown')}\n"
                   f"Author: {meta.get('author_name', 'Unknown')}\n"
                   f"Date: {meta.get('upload_date', 'Unknown')}\n"
                   f"URL: {meta.get('video_url', 'Unknown')}\n\n"
                   f"--- REDACTED TRANSCRIPT ---\n"
                   f"{text_only}"
                   f"--- ENHANCED NOTES ---\n"
                   f"{st.session_state.get('enhanced_text', '')}")
        
    return payload

def prepare_quiz_payload() -> str:
    """Combines metadata and the generated Markdown notes into a single string for the Quiz LLM."""
    meta = st.session_state.get("metadata", {})
    
    # Extract the generated notes from Step 2
    notes_text = st.session_state.get("enhanced_text", "")
    
    payload = (
        f"--- METADATA ---\n"
        f"Title: {meta.get('title', 'Unknown')}\n"
        f"Author: {meta.get('author_name', 'Unknown')}\n"
        f"Date: {meta.get('upload_date', 'Unknown')}\n"
        f"URL: {meta.get('video_url', 'Unknown')}\n\n"
        f"--- ENHANCED NOTES ---\n"
        f"{notes_text}"
    )
    return payload


def check_answer(user_choice: str, correct_answer: str) -> bool:
    """Robust fallback logic to check if the answer is correct despite formatting differences."""
    if user_choice == "I don't know":
        return False
        
    u = str(user_choice).strip().lower()
    c = str(correct_answer).strip().lower()
    
    if u == c: 
        return True
    # If the LLM output "B" but the user string is "B. To combine..."
    if u.startswith(f"{c}.") or u.startswith(f"{c})"): 
        return True
    # If the correct answer text is hiding inside the user's selected string
    if c in u: 
        return True
        
    return False

def bg_fetch_question(shared_queue, shared_status, payload, history, sys_prompt, text_model, temp, max_tok, num_opts, llm_manager):
    """Runs in a parallel thread. Fetches the next question and routes errors to the UI."""
    shared_status["running"] = True
    shared_status["error"] = None # Clear old errors
    
    try:
        context = "History of asked questions and user performance:\n"
        if history:
            for idx, h in enumerate(history):
                u_ans = h.get('user_choice', 'Currently Answering...')
                c_ans = h.get('answer', 'Unknown')
                context += f"Q{idx+1}: {h.get('question')}\nUser Answered: {u_ans} | Correct Answer: {c_ans}\n\n"
        else:
            context += "No previous questions.\n"

        dynamic_prompt = (
            f"{sys_prompt}\n\n{context}\n\n"
            f"CRITICAL INSTRUCTION: Generate EXACTLY 1 new question with EXACTLY {num_opts} possible options. "
            f"Your JSON object MUST contain an 'options' array with exactly {num_opts} strings. "
            f"ONLY return a valid JSON object."
        )

        full_text = llm_manager.generate_sync(payload, dynamic_prompt, text_model, temp, max_tok)

        start = full_text.find('{')
        end = full_text.rfind('}')
        if start != -1 and end != -1:
            norm_q = {str(k).lower().strip(): v for k, v in json.loads(full_text[start:end+1]).items()}
            if "options" in norm_q and isinstance(norm_q["options"], list):
                shared_queue.append(norm_q)
            else:
                raise ValueError("LLM failed to return a valid options array.")
        else:
            raise ValueError(f"No JSON brackets found. Raw: {full_text}")
            
    except Exception as e:
        # Route the error to the dictionary so the Streamlit UI can display it!
        shared_status["error"] = str(e)
    finally:
        shared_status["running"] = False


def build_quiz_context(history, queue):
    """Prunes history to ONLY the question text, user performance, and liking score to save tokens and prevent repetition."""
    context = "Questions already asked or currently in queue (DO NOT REPEAT THESE):\n"
    if not history and not queue:
        return context + "None.\n"
    
    # 1. Add historical questions
    for i, h in enumerate(history):
        q_text = h.get('question', 'Unknown Question')
        skipped = h.get('user_choice') == "I don't know"
        is_correct = h.get('is_correct', False)
        score = h.get('like_score', 0)
        
        status = "Skipped" if skipped else ("Correct" if is_correct else "Wrong")
        context += f"- {q_text} (User Status: {status}, Liking Score: {score}/100)\n"
        
    # 2. Add queued questions (so the LLM doesn't generate duplicates of what's already waiting!)
    for q in queue:
        context += f"- {q.get('question', 'Unknown Question')} (Status: In Queue)\n"
        
    return context

def bg_fetch_batch(shared_queue, shared_status, payload, history, sys_prompt, text_model, temp, max_tok, num_opts, batch_size, llm_manager):
    """Runs in parallel. Fetches a BATCH of questions and routes errors/payloads to the UI."""
    shared_status["running"] = True
    shared_status["error"] = None 
    
    try:
        context = build_quiz_context(history, shared_queue)

        dynamic_prompt = (
            f"{sys_prompt}\n\n{context}\n\n"
            f"CRITICAL INSTRUCTION: Generate EXACTLY a JSON array of {batch_size} new questions. "
            f"Each question MUST have exactly {num_opts} options. "
            f"Do NOT repeat any questions from the context above. If the user got previous questions 'Wrong' or 'Skipped', focus your new questions on those concepts. "
            f"Format strictly as a JSON list of objects:\n"
            f"[\n  {{\"question\": \"...\", \"options\": [\"A\", \"B\"...], \"answer\": \"...\", \"explanation\": \"...\"}}\n]"
        )

        # Save the exact prompt being sent so the user can debug it in the UI
        shared_status["last_payload"] = f"{payload}\n\n--- DYNAMIC PROMPT ---\n{dynamic_prompt}"

        full_text = llm_manager.generate_sync(payload, dynamic_prompt, text_model, temp, max_tok)

        # Extract the JSON array [...]
        start = full_text.find('[')
        end = full_text.rfind(']')
        if start != -1 and end != -1:
            raw_batch = json.loads(full_text[start:end+1])
            for raw_q in raw_batch:
                norm_q = {str(k).lower().strip(): v for k, v in raw_q.items()}
                if "options" in norm_q and isinstance(norm_q["options"], list):
                    shared_queue.append(norm_q) # Add each parsed question to the queue
        else:
            raise ValueError(f"No JSON array brackets found. Raw: {full_text}")
            
    except Exception as e:
        shared_status["error"] = str(e)
    finally:
        shared_status["running"] = False