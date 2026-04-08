import streamlit as st
import os
import json
import base64
import requests
from dotenv import load_dotenv
from pyzotero import zotero
import pymupdf4llm
from docling.document_converter import DocumentConverter

from shared_ui import render_enhancement_step, render_quiz_step, get_quiz_payload
import AI_manager as manager

# 1. LOAD ENVIRONMENT VARIABLES
load_dotenv()
ZOTERO_LIB_ID = os.getenv("ZOTERO_LIB_ID", "")
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY", "")

# 2. DEFINE MASTER DIRECTORY STRUCTURE
BASE_PDF_DIR = "saved_pdfs"
os.makedirs(BASE_PDF_DIR, exist_ok=True)

@st.cache_resource
def get_manager(): return manager.Manager()
ai_manager = get_manager()

# --- STATE INITIALIZATION ---
if "pdf_metadata" not in st.session_state:
    st.session_state.pdf_metadata = {}
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "pdf_markdown" not in st.session_state:
    st.session_state.pdf_markdown = ""

# --- HELPER FUNCTIONS ---
def setup_doc_folder(doc_id: str, is_batch: bool = False) -> dict:
    """Creates the specific folder structure for a given PDF."""
    # Route to 'unchecked' if it's a batch process
    base_dir = os.path.join(BASE_PDF_DIR, "unchecked") if is_batch else BASE_PDF_DIR
    
    doc_folder = os.path.join(base_dir, doc_id)
    img_folder = os.path.join(doc_folder, "images")
    os.makedirs(img_folder, exist_ok=True)
    
    return {
        "folder": doc_folder,
        "pdf_path": os.path.join(doc_folder, f"{doc_id}.pdf"),
        "md_path": os.path.join(doc_folder, f"{doc_id}.md"),
        "img_folder": img_folder,
        "meta_path": os.path.join(doc_folder, "metadata.json")
    }

def run_batch_pipeline(zot, parser_choice="PyMuPDF4LLM"):
    """Downloads, parses, and fetches metadata for all Zotero items."""
    st.info("Fetching all items from Zotero. This might take a moment...")
    
    # zot.everything() handles pagination to get the entire library
    all_items = zot.everything(zot.top()) 
    total_items = len(all_items)
    
    if total_items == 0:
        st.warning("Your Zotero library is empty.")
        return

    progress_bar = st.progress(0, text="Starting batch process...")
    
    for i, item in enumerate(all_items):
        item_key = item['key']
        title = item['data'].get('title', 'Untitled').replace("/", "_").replace("\\", "_")
        doi = item['data'].get('DOI', '')
        
        # Update progress
        progress_bar.progress((i + 1) / total_items, text=f"Processing {i+1}/{total_items}: {title}")
        
        paths = setup_doc_folder(item_key, is_batch=True)
        
        # 1. METADATA EXTRACTION
        metadata = {"title": title, "DOI": doi, "status": "unchecked"}
        if doi:
            crossref_data = fetch_crossref_metadata(doi)
            if crossref_data:
                metadata.update(crossref_data)
                
        with open(paths["meta_path"], "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
            
        # 2. PDF DOWNLOAD
        if not os.path.exists(paths["pdf_path"]):
            children = zot.children(item_key)
            pdf = next((c for c in children if c['data'].get('contentType') == 'application/pdf'), None)
            if pdf:
                try:
                    file_bytes = zot.file(pdf['key'])
                    with open(paths["pdf_path"], "wb") as f:
                        f.write(file_bytes)
                except Exception as e:
                    st.toast(f"Failed to download PDF for {title}: {e}")
                    continue # Skip to next item if download fails
            else:
                continue # Skip items without PDFs
                
        # 3. PARSING
        if not os.path.exists(paths["md_path"]) and os.path.exists(paths["pdf_path"]):
            try:
                if "PyMuPDF" in parser_choice:
                    md_text = pymupdf4llm.to_markdown(
                        doc=paths["pdf_path"],
                        write_images=True,
                        image_path=paths["img_folder"]
                    )
                else:
                    converter = DocumentConverter()
                    result = converter.convert(paths["pdf_path"])
                    md_text = result.document.export_to_markdown()
                    
                with open(paths["md_path"], "w", encoding="utf-8") as f:
                    f.write(md_text)
            except Exception as e:
                st.toast(f"Failed to parse {title}: {e}")

    progress_bar.progress(1.0, text="✅ Batch processing complete!")
    st.success(f"Successfully processed your Zotero library into the 'unchecked' folder.")

def display_pdf_iframe(pdf_path: str):
    """Renders a PDF file natively in a Streamlit column using base64."""
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # The #toolbar=0 hides the print/download buttons for a cleaner look
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="800px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def fetch_crossref_metadata(doi: str) -> dict:
    """Fetches academic metadata using a DOI via the Crossref API."""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Throws an error if the request fails
        data = response.json()["message"]
        return {
            "title": data.get("title", [""])[0],
            "authors": ", ".join([f"{a.get('given', '')} {a.get('family', '')}" for a in data.get("author", [])]),
            "year": data.get("created", {}).get("date-parts", [[None]])[0][0],
            "DOI": doi
        }
    except Exception as e:
        st.error(f"Failed to fetch Crossref data: {e}")
        return {}
    
# ==========================================
# UI LAYOUT
# ==========================================
st.title("📄 PDF Pipeline")

# Only show the ingestion UI if we haven't locked in a document yet
if not st.session_state.doc_id:
    st.header("Step 1: Document Ingestion")
    ingest_mode = st.radio("Select Source:", ["Zotero Library", "Manual Upload", "Batch Process Zotero (All)"])
    
    if ingest_mode == "Batch Process Zotero (All)":
        st.warning("⚠️ This will download and parse your ENTIRE Zotero library. The results will be saved in the 'unchecked' folder. This may take a long time depending on your library size.")
        z_type = st.selectbox("Library Type", ["user", "group"], key="batch_z_type")
        batch_parser = st.selectbox("Select Batch Parsing Engine", ["PyMuPDF4LLM (Recommended)", "Docling (OCR-heavy)"])
        
        if st.button("🚀 Start Full Batch Process", type="primary") and ZOTERO_LIB_ID and ZOTERO_API_KEY:
            try:
                zot = zotero.Zotero(ZOTERO_LIB_ID, z_type, ZOTERO_API_KEY)
                run_batch_pipeline(zot, parser_choice=batch_parser)
            except Exception as e:
                st.error(f"Failed to connect to Zotero: {e}")

    elif ingest_mode == "Zotero Library":
        st.info("Using credentials from .env file.")
        z_type = st.selectbox("Library Type", ["user", "group"])
        
        if st.button("Fetch Recent Items") and ZOTERO_LIB_ID and ZOTERO_API_KEY:
            try:
                zot = zotero.Zotero(ZOTERO_LIB_ID, z_type, ZOTERO_API_KEY)
                st.session_state.zotero_items = zot.top(limit=50)
            except Exception as e:
                st.error(f"Failed to connect to Zotero: {e}")
                
        if "zotero_items" in st.session_state:
            options = {item['key']: item['data'].get('title', 'Untitled') for item in st.session_state.zotero_items}
            sel_key = st.selectbox("Select Paper", options=list(options.keys()), format_func=lambda x: options[x])
            
            if st.button("Download & Initialize", type="primary"):
                with st.spinner("Downloading PDF from Zotero..."):
                    zot = zotero.Zotero(ZOTERO_LIB_ID, z_type, ZOTERO_API_KEY)
                    item = zot.item(sel_key)
                    
                    # 1. Set Metadata and ID
                    safe_title = item['data'].get('title', 'Untitled').replace("/", "_").replace("\\", "_")
                    st.session_state.doc_id = sel_key
                    st.session_state.pdf_metadata = {"title": safe_title, "DOI": item['data'].get('DOI', '')}

                    paths = setup_doc_folder(st.session_state.doc_id, is_batch=False)
                    with open(paths["meta_path"], "w", encoding="utf-8") as f:
                        json.dump(st.session_state.pdf_metadata, f, indent=4)
                                        
                    # 2. Setup folders
                    paths = setup_doc_folder(st.session_state.doc_id, is_batch=False)
                    
                    # ADD THIS CHECK: If the file is already there, skip downloading.
                    if os.path.exists(paths["pdf_path"]):
                        st.success("PDF already exists locally. Loading from cache...")
                        st.rerun()
                    else:
                        # 3. Download to folder (Your existing logic)
                        children = zot.children(sel_key)
                        pdf = next((c for c in children if c['data'].get('contentType') == 'application/pdf'), None)
                        if pdf:
                            file_bytes = zot.file(pdf['key'])
                            with open(paths["pdf_path"], "wb") as f:
                                f.write(file_bytes)
                            st.rerun()
                        else:
                            st.error("No PDF attachment found for this Zotero item.")

    elif ingest_mode == "Manual Upload":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file and st.button("Initialize PDF", type="primary"):
            # Use filename without extension as the ID
            raw_name = uploaded_file.name.rsplit(".", 1)[0]
            st.session_state.doc_id = raw_name
            st.session_state.pdf_metadata = {"title": raw_name}

            paths = setup_doc_folder(st.session_state.doc_id, is_batch=False)
            
            # Save uploaded bytes to the dedicated folder
            with open(paths["pdf_path"], "wb") as f:
                f.write(uploaded_file.getvalue())
            st.rerun()

# ==========================================
# PARSING & SIDE-BY-SIDE VIEW
# ==========================================
else:
    paths = setup_doc_folder(st.session_state.doc_id, is_batch=False)

    # If we have no markdown in memory, but the file exists on disk, load it!
    if not st.session_state.pdf_markdown and os.path.exists(paths["md_path"]):
        with open(paths["md_path"], "r", encoding="utf-8") as f:
            st.session_state.pdf_markdown = f.read()
        st.toast("Loaded parsed markdown from cache!", icon="⚡")

    st.markdown(f"### 📑 {st.session_state.pdf_metadata.get('title')}")
    if st.button("🔙 Close & Ingest New PDF"):
        st.session_state.doc_id = None
        st.session_state.pdf_markdown = ""
        st.rerun()
        
    st.divider()
    
    # Create Side-by-Side Layout
    col_pdf, col_text = st.columns([1, 1])
    
    with col_pdf:

        # PARSER CONTROLS
        parse_col1, parse_col2 = st.columns([2, 1])
        with parse_col1:
            parser_choice = st.selectbox("Select Parsing Engine", ["PyMuPDF4LLM (Recommended)", "Docling (OCR-heavy)"])
        with parse_col2:
            if st.button("▶️ Run Parser", use_container_width=True):
                with st.spinner(f"Parsing with {parser_choice}..."):
                    if "PyMuPDF" in parser_choice:
                        # PyMuPDF extracts markdown AND saves images automatically!
                        md_text = pymupdf4llm.to_markdown(
                            doc=paths["pdf_path"],
                            write_images=True,
                            image_path=paths["img_folder"]
                        )
                        st.session_state.pdf_markdown = md_text
                    
                    elif "Docling" in parser_choice:
                        converter = DocumentConverter()
                        result = converter.convert(paths["pdf_path"])
                        st.session_state.pdf_markdown = result.document.export_to_markdown()
                    
                    # Save the generated markdown to disk immediately
                    with open(paths["md_path"], "w", encoding="utf-8") as f:
                        f.write(st.session_state.pdf_markdown)
                st.success("Parsing complete and markdown saved!")
                st.rerun()
        
        st.subheader("Source Document")
        if os.path.exists(paths["pdf_path"]):
            display_pdf_iframe(paths["pdf_path"])
        else:
            st.error("PDF file missing from disk.")

        # get the DOI from metadata and offer to fetch more details if not already present
        st.divider()
        with st.expander("🔗 Fetch Metadata via DOI (Crossref)"):
            
            # 1. GRAB EXISTING DOI (Defaults to empty string if not found)
            existing_doi = st.session_state.pdf_metadata.get("DOI", "")
            
            # 2. INJECT IT INTO THE TEXT INPUT
            doi_input = st.text_input(
                "Enter DOI", 
                value=existing_doi  # <--- This auto-compiles the box!
            )
            
            if st.button("Fetch & Save Metadata"):
                if doi_input:
                    with st.spinner("Fetching from Crossref..."):
                        new_meta = fetch_crossref_metadata(doi_input.strip())
                        if new_meta:
                            st.session_state.pdf_metadata.update(new_meta)
                            with open(paths["meta_path"], "w", encoding="utf-8") as f:
                                json.dump(st.session_state.pdf_metadata, f, indent=4)
                            st.success("Metadata updated and saved!")
                            st.rerun()

    with col_text:
        st.subheader("Extracted Markdown")

        # SYNCED ZOOM CONTROLS
        def sync_zoom(key):
            st.session_state.global_zoom = st.session_state[key]
        st.slider("🔍 Zoom Text Size", min_value=10, max_value=50, value=st.session_state.get("global_zoom", 16), key="zoom_pdf_step1", on_change=sync_zoom, args=("zoom_pdf_step1",), label_visibility="collapsed")
        
        st.markdown(f"""
            <style>
                .stTextArea textarea {{ font-size: {st.session_state.get('global_zoom', 16)}px !important; line-height: 1.5 !important; }}
                .stMarkdown p, .stMarkdown li {{ font-size: {st.session_state.get('global_zoom', 16)}px !important; line-height: 1.5 !important; }}
            </style>
        """, unsafe_allow_html=True)

        # TEXT EDITOR / VIEWER
        if st.session_state.pdf_markdown:
            is_preview_mode = st.toggle("👁️ Preview Formatting Mode", value=False)
            
            def save_md_edits():
                st.session_state.pdf_markdown = st.session_state.pdf_edit_area
                with open(paths["md_path"], "w", encoding="utf-8") as f:
                    f.write(st.session_state.pdf_markdown)
            
            if is_preview_mode:
                # Render the markdown visually
                with st.container(height=650, border=True):
                    st.markdown(st.session_state.pdf_markdown, unsafe_allow_html=True)
            else:
                # Editable text area synced to disk
                st.text_area(
                    "Edit Markdown", 
                    value=st.session_state.pdf_markdown, 
                    height=800, 
                    key="pdf_edit_area", 
                    on_change=save_md_edits,
                    label_visibility="collapsed"
                )

# ==========================================
# DOWNSTREAM PIPELINE (Shared UI)
# ==========================================
if st.session_state.pdf_markdown:
    
    # Callbacks for shared UI
    def pdf_get_llm_payload(enhanced=False):
        base = f"Title: {st.session_state.pdf_metadata.get('title')}\n\nDocument Text:\n{st.session_state.pdf_markdown}"
        if enhanced and st.session_state.get('enhanced_text'):
            return f"{base}\n\nCurrent Notes:\n{st.session_state.enhanced_text}"
        return base

    # Then call the shared UI, passing this specific function:
    render_enhancement_step(
        doc_id=st.session_state.doc_id, 
        doc_title=st.session_state.pdf_metadata.get('title', 'PDF_Note'), 
        manager=ai_manager, 
        get_payload_func=pdf_get_llm_payload,  
        default_prompt="Obsidian_Academic_Note", 
        default_temp=0.7,                     
        default_tokens=8000,
        CACHE_DIR = paths["folder"]  # Pass the specific folder for this document
    )
    
    render_quiz_step(
        doc_id=st.session_state.doc_id, 
        manager=ai_manager, 
        get_quiz_payload_func=get_quiz_payload,
        CACHE_DIR = paths["folder"]  # Pass the specific folder for this document
    )