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

from youtube_transcript_api import YouTubeTranscriptApi


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

def fetch_transcript_with_logs(url: str, video_id: str) -> dict:
    """
    Fetches transcript using the free youtube-transcript-api 
    and grabs metadata using YouTube's free oEmbed endpoint.
    """
    st.write(f"🔍 Starting extraction for video ID: `{video_id}`...")
    
    # --- 1. Fetch Metadata (oEmbed) ---
    st.write("📊 Fetching video metadata (title, author)...")
    metadata = {
        "title": "Unknown Title",
        "author_name": "Unknown Channel",
        "video_url": url,
        "upload_date": "Unknown"
    }
    
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            metadata["title"] = data.get("title", metadata["title"])
            metadata["author_name"] = data.get("author_name", metadata["author_name"])
            st.write(f"✅ Found video: **{metadata['title']}**")
        else:
            st.warning("⚠️ Could not fetch complete metadata, proceeding with defaults.")
    except Exception as e:
        st.warning(f"⚠️ Metadata fetch error: {e}")

    # --- 2. Fetch Transcript ---
    st.write("🌐 Calling free YouTube Transcript API...")
    try:
        yt_api = YouTubeTranscriptApi()
        raw_transcript = yt_api.fetch(video_id)
        
        segments = []
        for item in raw_transcript:
            segments.append({
                # CHANGED: We now access these as object attributes instead of dict keys
                "start": getattr(item, "start", 0.0), 
                "text": getattr(item, "text", "")
            })
        
        st.success(f"✅ Successfully extracted {len(segments)} transcript segments!")
        return {
            "segments": segments,
            "metadata": metadata
        }
        
    except Exception as e:
        # Pushing the exact error to the UI so the user can read it
        st.error(f"❌ Transcript extraction failed! Error: {e}")
        st.info("💡 Hint: This usually happens if the video has subtitles disabled by the creator, is age-restricted, or is a live stream.")
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
        
        if st.button("Save Prompt", width='stretch'):
            if new_prompt_name and system_prompt:
                save_prompt(PROMPTS_FILE, new_prompt_name, system_prompt)
                st.success("Saved!")
                st.rerun()

    return model, temperature, max_tokens, streaming_on, system_prompt

# Helper function to avoid duplicating the generation code
def run_generation(manager, payload, system_prompt, model_name, temperature, max_tokens, streaming_on):
    """
    Generates the enhanced note using the selected LLM.
    Returns the final text string to be saved in session state.
    """
    try:
        if streaming_on:
            # Create an empty container to hold the streaming text
            placeholder = st.empty()
            full_text = ""
            
            # Stream the response chunk by chunk
            for chunk in manager.generate_stream(payload, system_prompt, model_name, temperature, max_tokens):
                full_text += chunk
                # Add a blinking cursor effect for better UX
                placeholder.markdown(full_text + "▌") 
            
            # Print the final text without the cursor
            placeholder.markdown(full_text)
            st.toast("✅ Generation complete!", icon="🧠")
            return full_text
            
        else:
            # Sync generation (no streaming)
            with st.spinner("🧠 Generating AI Note..."):
                full_text = manager.generate_sync(payload, system_prompt, model_name, temperature, max_tokens)
                st.markdown(full_text)
                st.toast("✅ Generation complete!", icon="🧠")
                return full_text
                
    except Exception as e:
        st.error(f"❌ AI Generation Failed: {e}")
        return None


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