import os
import re
import json
import requests
import streamlit as st
import AI_manager as manager

import os
import hashlib
import trafilatura
from urllib.parse import urlparse

## --- YOUTUBE UTILS ---

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

def get_cached_videos(cache_dir: str) -> dict:
    """
    Scans the cache directory for saved video JSON files.
    Returns a dictionary mapping 'video_id' to its 'title'.
    This is used to populate the dropdown menu in the UI.
    """
    cached_videos = {}
    
    if not os.path.exists(cache_dir):
        return cached_videos
        
    for filename in os.listdir(cache_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(cache_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Extract the video ID from the filename (remove .json)
                video_id = filename.replace(".json", "")
                
                # Try to get the title from metadata, default to the ID if not found
                title = data.get("metadata", {}).get("title", f"Unknown Title ({video_id})")
                
                cached_videos[video_id] = title
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return cached_videos

def load_cached_video(cache_dir: str, video_id: str) -> dict:
    """
    Reads a specific video's JSON file from disk and returns the dictionary.
    """
    filepath = os.path.join(cache_dir, f"{video_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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
        


## --- WEBSITE UTILS ---

def get_url_hash(url: str) -> str:
    """
    Converts a URL into a safe, unique string using SHA-256.
    This prevents file path errors caused by special characters in URLs.
    """
    return hashlib.sha256(url.encode('utf-8')).hexdigest()

def scrape_website_to_markdown(BASE_WEB_DIR: str, url: str) -> dict:
    """
    Downloads a webpage and extracts its core content into Markdown.
    Includes caching to prevent redundant network calls.
    """
    # 1. Validate the URL format basically
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return {"error": "Invalid URL provided. Please include http:// or https://", "markdown": None, "folder": None}

    # 2. Setup caching paths
    url_hash = get_url_hash(url)
    doc_folder = os.path.join(os.getcwd(), BASE_WEB_DIR, url_hash)
    md_path = os.path.join(doc_folder, f"{url_hash}.md")
    
    # 3. Check Cache
    if os.path.exists(md_path):
        # If we already scraped this, just read it from the local disk
        with open(md_path, "r", encoding="utf-8") as f:
            cached_md = f.read()
        return {"error": None, "markdown": cached_md, "folder": doc_folder}

    # 4. Fetch and Extract (Network Call)
    # trafilatura.fetch_url handles basic timeouts and network errors
    downloaded = trafilatura.fetch_url(url)
    
    if downloaded is None:
         return {"error": "Failed to fetch the webpage. It might be blocking scrapers (403 Forbidden) or timing out.", "markdown": None, "folder": None}

    # Extract the content and output directly as Markdown!
    # This ignores navbars, footers, and ads automatically.
    markdown_content = trafilatura.extract(downloaded, output_format="markdown")
    
    if not markdown_content:
        return {"error": "Successfully fetched the page, but could not extract readable article content.", "markdown": None, "folder": None}

    # 5. Save to Cache
    os.makedirs(doc_folder, exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    return {"error": None, "markdown": markdown_content, "folder": doc_folder}


    
## --- SHARED UTILS ---

def format_timestamp(seconds) -> str:
    """Helper function to format seconds into MM:SS format."""
    try:
        sec_float = float(seconds)
        mins = int(sec_float // 60)
        secs = int(sec_float % 60)
        return f"{mins:02d}:{secs:02d}"
    except (ValueError, TypeError):
        return "00:00"

def load_prompts(filepath: str) -> dict:
    """Loads system prompts. Creates default Obsidian and Quiz prompts if missing."""

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                prompts = json.load(f)
                return prompts
        except Exception:
            pass
    # If file doesn't exist or is corrupted, return an error
    st.warning("⚠️ System prompts file missing or unreadable. Please fill it with valid JSON prompts.")
    return {}

def save_prompt(filepath: str, name: str, prompt_text: str):
    """Saves a new or updated prompt to the JSON file."""
    prompts = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            prompts = json.load(f)
    prompts[name] = prompt_text
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=4)





def llm_settings(manager: manager.Manager, default_model: str, default_temp: float, default_max_tokens: int, PROMPTS_FILE: str, default_prompt: str):
    """Renders the LLM settings UI and updates session state on change."""
    st.subheader("⚙️ LLM Settings")

    available_models = manager.get_models()
    default_models = ["No models found"] if not available_models else available_models
    model = st.selectbox("Model", options=default_models, index=manager.get_models().index(default_model))
        
    temperature = st.number_input("Temperature", 0.0, 10.0, default_temp, 0.1)
    max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 100000, default_max_tokens, 100)
    streaming_on = st.toggle("Streaming Generation", value=True)

    st.subheader("System Prompts")
    prompts_dict = load_prompts(PROMPTS_FILE)
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
                save_prompt(PROMPTS_FILE, new_prompt_name, system_prompt)
                st.success("Saved!")
                st.rerun()

    return model, temperature, max_tokens, streaming_on, system_prompt

# Helper function to avoid duplicating the generation code
def run_generation(manager, llm_payload, system_prompt, model, temperature, max_tokens, cached_path, streaming_on):

    st.session_state.enhanced_text = ""
    text_placeholder = st.empty()
    
    if streaming_on:
        full_text = ""
        with st.status(f"Generative pass using {model}...", expanded=True) as status:
            for chunk in manager.generate_stream(llm_payload, system_prompt, model, temperature, max_tokens):
                full_text += chunk
                text_placeholder.markdown(full_text + "▌") 
            status.update(label="Complete!", state="complete", expanded=False)
        text_placeholder.empty() 
        st.session_state.enhanced_text = full_text
    else:
        with st.status(f"Generating Output...", expanded=True) as status:
            st.session_state.enhanced_text = manager.generate_sync(llm_payload, system_prompt, model, temperature, max_tokens)
            status.update(label="Complete!", state="complete", expanded=False)

    # Save the new text to disk or overwrite existing file
    with open(cached_path, "w", encoding="utf-8") as f:
        f.write(st.session_state.enhanced_text)
    st.toast("Generation complete and saved!", icon="✅")
    st.rerun() # Refresh UI to show the new text


# Callbacks for shared UI
def pdf_get_llm_payload(enhanced=False) -> str:
        """Combines PDF metadata and parsed markdown into a single string for the LLM."""
        meta = st.session_state.pdf_metadata
        document_text = st.session_state.pdf_markdown
        
        # 1. TOP BREAD: The Data
        payload = (
            f"--- METADATA ---\n"
            f"Title: {meta.get('title', 'Unknown Title')}\n"
            f"Authors: {meta.get('authors', 'Unknown Authors')}\n"
            f"Year: {meta.get('year', 'Unknown Year')}\n"
            f"DOI: {meta.get('DOI', 'None')}\n\n"
            f"--- SOURCE DOCUMENT ---\n"
            f"{document_text}\n"
        )
        
        if enhanced and st.session_state.get('enhanced_text'):
            payload += (
                f"\n--- EXISTING ENHANCED NOTES ---\n"
                f"{st.session_state.enhanced_text}\n"
            )
            
        # 2. BOTTOM BREAD: The Ultimate Override Command
        # This is the last thing the model reads before generating.
        payload += (
            f"\n\n=========================================\n"
            f"SYSTEM OVERRIDE COMMAND:\n"
            f"You have finished reading the source document.\n"
            f"You MUST now output the notes using the EXACT Markdown template provided in your system instructions.\n"
            f"DO NOT write conversational text. DO NOT write paragraphs.\n"
            f"START YOUR OUTPUT IMMEDIATELY WITH '# [[Title]]'.\n"
            f"=========================================\n"
        )
            
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

def bg_fetch_answers(shared_status, payload, questions_list, sys_prompt, text_model, temp, max_tok, num_opts, llm_manager):
    """Runs in parallel. Takes the Qmodel strings and generates the full JSON quiz."""
    shared_status["running"] = True
    shared_status["done"] = False
    shared_status["error"] = None
    
    try:
        a_prompt = (
            f"{sys_prompt}\n\n"
            f"CRITICAL INSTRUCTION: Build a multiple-choice quiz for EXACTLY the following {len(questions_list)} questions:\n"
            f"{json.dumps(questions_list, indent=2)}\n\n"
            f"Each question MUST have exactly {num_opts} options. "
            f"Format strictly as a JSON list of objects:\n"
            f"[\n  {{\"question\": \"[Insert Question text here]\", \"options\": [\"A\", \"B\"...], \"answer\": \"...\", \"explanation\": \"...\"}}\n]"
        )
        
        # Save the exact payload for UI transparency
        shared_status["last_payload"] = f"--- A-MODEL SYSTEM PROMPT ---\n{a_prompt}\n\n--- DOCUMENT PAYLOAD ---\n{payload}"
        
        a_output = llm_manager.generate_sync(payload, a_prompt, text_model, temp, max_tok)
        
        start_a = a_output.find('[')
        end_a = a_output.rfind(']')
        if start_a != -1 and end_a != -1:
            raw_batch = json.loads(a_output[start_a:end_a+1])
            shared_status["result"] = [{str(k).lower().strip(): v for k, v in q.items()} for q in raw_batch]
        else:
            raise ValueError(f"A-Model failed to return a JSON array. Raw: {a_output}")
            
    except Exception as e:
        shared_status["error"] = str(e)
    finally:
        shared_status["running"] = False
        shared_status["done"] = True