import os
import re
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from streamlit_player import st_player

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

# ==========================================
# 2. MODULAR FUNCTIONS (Business Logic)
# ==========================================

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

def fetch_transcript_with_logs(video_url: str, video_id: str) -> dict:
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
    
def save_edits_to_disk():
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

# ==========================================
# 4. UI LAYOUT & INTERACTION
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    input_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Fetch & Process Transcript", type="primary"):
        if input_url.strip():  
            video_id = extract_video_id(input_url)
            st.session_state.video_url = input_url
            st.session_state.video_id = video_id
            
            with st.status("Processing Request...", expanded=True) as status:
                full_data_dict = fetch_transcript_with_logs(video_url=input_url, video_id=video_id) 
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
        st.divider()

        st.subheader("🛠️ Quick Tools")
        st.markdown("**Add Section Header**")
        sect_col1, sect_col2 = st.columns([3, 2])
        with sect_col1:
            section_name = st.text_input("Section Name", key="section_input_field", label_visibility="collapsed", placeholder="e.g. Intro")
        with sect_col2:
            if st.button("Add", use_container_width=True):
                if section_name.strip() and len(st.session_state.transcript) > 0:
                    for idx, seg in enumerate(st.session_state.transcript):
                        if seg.get('start', 0.0) == st.session_state.start_time:
                            st.session_state.transcript[idx]['text'] = f"### - {section_name}\n\n{seg['text']}"
                            
                            # <-- NEW: Save the header addition to disk
                            save_edits_to_disk()
                            st.toast("💾 Section added & saved!", icon="✅")
                            
                            st.rerun()

# --- Main Layout ---
st.title("🎬 YouTube Transcript Editor")

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
            timestamp_str = format_timestamp(start_sec)
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
                    save_edits_to_disk()
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
            
            
    # --- Copy Output ---
    st.divider()
    final_text = format_transcript_for_copy(st.session_state.transcript)
    st.caption("Hover over the box below and click the copy icon on the top right.")
    st.code(final_text, language="text")

else:
    st.info("👈 Enter a YouTube URL in the sidebar and click 'Fetch' to begin.")

