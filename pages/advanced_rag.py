import streamlit as st
import os
import AI_manager as manager
import time
from datetime import timedelta
import shutil # For wiping existing DBs safely
import functions
import re # Needed for text highlighting
import json
import requests
import hashlib

# --- imports for the VectorDB ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# ---------------------------------------------------------
# UI SETUP & STATE MANAGEMENT
# ---------------------------------------------------------
st.set_page_config(page_title="Advanced RAG Pipeline", layout="wide")
st.title("Advanced RAG Pipeline Configurator")
st.markdown("Configure your data sources, embedding models, and chunking strategies with absolute transparency.")
st.markdown("---")

default_temp = 0.7
default_tokens = 8000

@st.cache_resource
def get_manager(): return manager.Manager()
ai_manager = get_manager()

# Initialize session state to carry our configuration across steps
if "rag_config" not in st.session_state:
    st.session_state.rag_config = {}

# ---------------------------------------------------------
# STEP 1: DATA SOURCE & MODEL SELECTION
# ---------------------------------------------------------
st.header("Step 1: Data Source & Model Selection for Vector Data Base")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Data Source Selection")
    
    # Initialize directory navigator state
    if 'current_path' not in st.session_state:
        st.session_state.current_path = os.path.abspath(os.getcwd())

    # Native Streamlit Directory Browser
    c_up, c_sel = st.columns([1, 4])
    with c_up:
        if st.button("⬆️ Up Dir"):
            st.session_state.current_path = os.path.dirname(st.session_state.current_path)
            st.rerun()
    with c_sel:
        try:
            # List only directories
            dirs = [d for d in os.listdir(st.session_state.current_path) if os.path.isdir(os.path.join(st.session_state.current_path, d))]
            dirs.insert(0, ".") # Default current dir option
        except PermissionError:
            dirs = ["."]
            st.error("Permission denied to read this directory.")
            
        selected_dir = st.selectbox("Navigate to subfolder:", dirs, label_visibility="collapsed")
        if selected_dir != ".":
            st.session_state.current_path = os.path.join(st.session_state.current_path, selected_dir)
            st.rerun()

    target_folder = st.text_input("Target Folder path:", st.session_state.current_path)
    st.session_state.rag_config['data_path'] = target_folder
    
    # Smart DB Existence Check
    db_path = os.path.join(target_folder, "chroma_db")
    db_exists = os.path.exists(db_path) and len(os.listdir(db_path)) > 0
    
    if db_exists:
        st.info("📦 Existing VectorDB found in this folder.")
        db_action = st.radio("Action:", ["Append new files only", "Wipe and Rebuild entirely"])
        st.session_state.rag_config['db_action'] = db_action
    else:
        st.info("✨ No existing VectorDB found. A new one will be created.")
        st.session_state.rag_config['db_action'] = "Create New"

with col2:
    st.subheader("🧠 Embedding Model Selection")
                
    available_models = ai_manager.get_models()
    default_models = ["No models found"] if not available_models else available_models
                
    embedding_idx = default_models.index("snowflake-arctic-embed2:568m") if "snowflake-arctic-embed2:568m" in default_models else 0
    embedding_type = st.selectbox("Embedding Model", default_models, index=embedding_idx, key="emb_model", help="Choose an embedding model compatible with your VectorDB. For ChromaDB, 1536-dim models like 'snowflake-arctic-embed2:568m' are ideal.")

    #llm_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0
    #llm_type = st.selectbox("LLM for RAG", default_models, index=llm_idx, key="llm_model")

    #st.divider()

    #temperature = st.number_input("Temperature", 0.0, 2.0, default_temp, 0.1)
    #max_tokens = st.number_input("Max Tokens (Verbosity)", 100, 10000, default_tokens, 100)
    #streaming_on = st.toggle("Streaming Generation", value=True)

    st.session_state.rag_config['embedding_type'] = embedding_type
    #st.session_state.rag_config['llm_type'] = llm_type

# ---------------------------------------------------------
# STEP 1b: EMBEDDING & CHUNKING PARAMETERS
# ---------------------------------------------------------
st.subheader("Embedding & Chunking Parameters")
st.info("Total transparency mode: No hidden defaults. Adjust your splitting logic precisely.")

with st.expander("⚙️ Splitting, Chunking & Embedding Parameters", expanded=True):
    c_col1, c_col2, c_col3 = st.columns(3)
    
    with c_col1:
        chunk_strategy = st.selectbox("Chunking Strategy", ["Recursive Character", "Token-Based", "Strict Character"])
        chunk_size = st.number_input("Chunk Size", min_value=100, max_value=8000, value=1300, step=100)
        chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=2000, value=350, step=50)
    
    with c_col2:
        if chunk_strategy in ["Recursive Character", "Strict Character"]:
            # Let user define exact separators, defaulting to standard Markdown structural breaks
            raw_separators = st.text_input("Separators (comma separated list, highest to lowest priority):", value="\n\n, \n, . ,  ,#, ##,###,")
            # Parse the string into actual escape characters
            separators = [sep.strip().replace('\\n', '\n') for sep in raw_separators.split(",")]
        else:
            st.info("Separators are intrinsically handled by the tokenizer for Token-Based splitting.")
            separators = None

    with c_col3:
        embedding_dimensions = st.number_input("Embedding Dimensions (if configurable)", min_value=128, max_value=8192, value=1536)
        distance_metric = st.selectbox("Distance Metric", ["Cosine Similarity", "L2 (Euclidean)", "Inner Product"])

# Save config button
if st.button("Save Step 1 Configuration and Execute Database Creation"):
    st.session_state.rag_config.update({
        'chunk_strategy': chunk_strategy,
        'chunk_size': chunk_size,
        'chunk_overlap': chunk_overlap,
        'separators': separators,
        'emb_model_name': embedding_type,
        'embedding_dimensions': embedding_dimensions,
        'distance_metric': distance_metric
    })
    st.success("✅ All parameters are now globally accessible in session state.")

    if not st.session_state.rag_config:
        st.error("⚠️ Please save your Step 1 Configuration first.")
    else:
        config = st.session_state.rag_config
        data_path = config['data_path']
        persist_directory = os.path.join(data_path, "chroma_db")
        db_action = config.get('db_action', "Create New")
        
        with st.spinner("Preparing pipeline..."):
            try:
                # 1. Initialize Embeddings and Chroma settings
                # embeddings = ai_manager.get_embedding(config['emb_model_name'])
                embeddings = OllamaEmbeddings(model=config['emb_model_name']) # Adjust based on how AI_manager handles embeddings

                metric_mapping = {"Cosine Similarity": "cosine", "L2 (Euclidean)": "l2", "Inner Product": "ip"}
                collection_metadata = {"hnsw:space": metric_mapping.get(config['distance_metric'], "cosine")}

                # 2. Handle DB Wiping if requested
                if db_action == "Wipe and Rebuild entirely" and os.path.exists(persist_directory):
                    shutil.rmtree(persist_directory)
                    st.toast("Old database wiped.")

                # 3. Initialize Chroma DB client
                vector_db = Chroma(
                    persist_directory=persist_directory, 
                    embedding_function=embeddings,
                    collection_metadata=collection_metadata
                )

                # 4. Load Markdown Files
                st.toast("Scanning for Markdown files...")
                loader = DirectoryLoader(data_path, glob="**/*.md", loader_cls=TextLoader)
                all_docs = loader.load()
                
                if not all_docs:
                    st.warning(f"No .md files found in {data_path}.")
                    time.sleep(1)
                    st.rerun()

                # 5. Filter out already embedded files (Smart Append)
                docs_to_process = all_docs
                if db_action == "Append new files only":
                    try:
                        existing_data = vector_db.get(include=["metadatas"])
                        if existing_data and existing_data['metadatas']:
                            existing_sources = set(meta.get('source') for meta in existing_data['metadatas'])
                            docs_to_process = [d for d in all_docs if d.metadata.get('source') not in existing_sources]
                    except Exception as e:
                        st.warning(f"Could not read existing DB metadata, processing all docs. Error: {e}")

                if not docs_to_process:
                    st.success("✅ Database is already up to date! No new files to embed.")
                    st.session_state.vector_db = vector_db
                    time.sleep(1)
                    st.rerun()

                st.info(f"📄 Found {len(docs_to_process)} new document(s) to process (out of {len(all_docs)} total).")

                # 6. Configure Splitter
                if config['chunk_strategy'] == "Recursive Character":
                    splitter = RecursiveCharacterTextSplitter(chunk_size=config['chunk_size'], chunk_overlap=config['chunk_overlap'], separators=config['separators'])
                elif config['chunk_strategy'] == "Strict Character":
                    splitter = CharacterTextSplitter(chunk_size=config['chunk_size'], chunk_overlap=config['chunk_overlap'], separator=config['separators'][0])
                else: 
                    splitter = TokenTextSplitter(chunk_size=config['chunk_size'], chunk_overlap=config['chunk_overlap'])

                # 7. Document-Level Batching & ETA Execution
                progress_bar = st.progress(0)
                status_text = st.empty()
                eta_text = st.empty()
                
                start_time = time.time()
                total_docs = len(docs_to_process)
                total_chunks_created = 0

                for i, doc in enumerate(docs_to_process):
                    # Process ONE document
                    chunks = splitter.split_documents([doc])
                    total_chunks_created += len(chunks)
                    
                    status_text.text(f"🧠 Splitting & Embedding document {i+1}/{total_docs}: {os.path.basename(doc.metadata.get('source', 'Unknown'))}...")
                    
                    if chunks:
                        vector_db.add_documents(chunks)
                    
                    # Update Progress & Calculate ETA
                    docs_completed = i + 1
                    progress_bar.progress(docs_completed / total_docs)
                    
                    elapsed_time = time.time() - start_time
                    avg_time_per_doc = elapsed_time / docs_completed
                    remaining_docs = total_docs - docs_completed
                    eta_seconds = int(avg_time_per_doc * remaining_docs)
                    
                    eta_str = str(timedelta(seconds=eta_seconds))
                    eta_text.text(f"⏱️ Estimated Time Remaining: {eta_str}")

                # Cleanup UI and Save State
                eta_text.empty()
                status_text.success(f"✅ Successfully processed {total_docs} document(s) into {total_chunks_created} chunks!")
                
                st.session_state.vector_db = vector_db
                st.success(f"✅ VectorDB loaded and ready at `{persist_directory}`!")

            except Exception as e:
                st.error(f"❌ An error occurred during VectorDB operations: {str(e)}")


# ---------------------------------------------------------
# STEP 2: THE QUERY ENHANCER (Adapted custom UI)
# ---------------------------------------------------------

PROMPTS_FILE = "system_prompts.json"

def init_enhancer_state():
    if "is_editing_enhanced" not in st.session_state:
        st.session_state.is_editing_enhanced = False
    if "global_zoom" not in st.session_state:
        st.session_state.global_zoom = 16 # Default font size

def sync_zoom(key):
    st.session_state.global_zoom = st.session_state[key]

def render_query_enhancement_step(
    manager, 
    default_prompt: str = "RAG_query",
    default_temp: float = 0.7,                       
    default_tokens: int = 1500
):
    init_enhancer_state()
    st.divider()
    st.header("✨ Step 2: Enhance Query via LLM")
    st.markdown("Brain-dump your main ideas below. The LLM will expand and optimize this into a highly semantic search query.")

    if 'vector_db' not in st.session_state:
        st.warning("⚠️ Please initialize or load your VectorDB in Step 1 before proceeding.")
        return

    # The Raw Input Payload
    raw_query = st.text_area("🧠 Your Raw Thoughts / Query:", height=100, placeholder="Type your messy, unstructured thoughts here...")
    
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

                temperature = st.number_input("Temperature", 0.0, 2.0, default_temp, 0.1, key="enh_temp")
                max_tokens = st.number_input("Max Tokens", 100, 10000, default_tokens, 100, key="enh_tokens")
                streaming_on = st.toggle("Streaming Generation", value=True, key="enh_stream")

            st.subheader("System Prompts")
            try:
                prompts_dict = functions.load_prompts(PROMPTS_FILE)
            except Exception as e:
                st.error(f"Could not load prompts: {e}")
                prompts_dict = {"RAG_query": "You are a search optimizer. Expand the following query with synonyms and semantic context."}
            
            prompt_names = list(prompts_dict.keys())
            default_idx = prompt_names.index(default_prompt) if default_prompt in prompt_names else 0
            
            if "text_prompt_area" not in st.session_state:
                st.session_state.text_prompt_area = prompts_dict.get(prompt_names[default_idx], "")

            def sync_prompt_to_area():
                selected = st.session_state.text_prompt_sel
                st.session_state.text_prompt_area = prompts_dict.get(selected, "")

            selected_prompt_name = st.selectbox(
                "Active Prompt", 
                prompt_names, 
                index=default_idx, 
                key="text_prompt_sel",
                on_change=sync_prompt_to_area
            )
            
            system_prompt = st.text_area("Edit Current Prompt", height=200, key="text_prompt_area")
            
            with st.expander("Save / Modify Prompt"):
                new_prompt_name = st.text_input("Save as (Prompt Name)", value=selected_prompt_name)
                if st.button("Save Prompt", use_container_width=True):
                    if new_prompt_name and system_prompt:
                        try:
                            functions.save_prompt(PROMPTS_FILE, new_prompt_name, system_prompt)
                            st.success("Saved!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save prompt: {e}")

            # GENERATE LOGIC
            if st.button("🚀 Generate Search Query", use_container_width=True, type="primary"):
                if not raw_query.strip():
                    st.error("Please enter your raw thoughts first.")
                else:
                    st.session_state.final_search_query = ""
                    text_placeholder = st.empty()
                    
                    if streaming_on:
                        full_text = ""
                        with st.status(f"Enhancing query using {text_model}...", expanded=True) as status:
                            try:
                                # Assuming your AI manager yields chunks
                                for chunk in manager.generate_stream(raw_query, system_prompt, text_model, temperature, max_tokens):
                                    full_text += chunk
                                    text_placeholder.markdown(f"<div style='font-size: {st.session_state.global_zoom}px;'>{full_text}▌</div>", unsafe_allow_html=True) 
                                status.update(label="Complete!", state="complete", expanded=False)
                            except Exception as e:
                                st.error(f"Generation error: {e}")
                        text_placeholder.empty() 
                        st.session_state.final_search_query = full_text
                    else:
                        with st.status(f"Generating Output...", expanded=True) as status:
                            try:
                                st.session_state.final_search_query = manager.generate_sync(raw_query, system_prompt, text_model, temperature, max_tokens)
                                status.update(label="Complete!", state="complete", expanded=False)
                            except Exception as e:
                                st.error(f"Generation error: {e}")

        with col_output:
            st.subheader("Enhanced Query Output")
            st.slider("🔍 Zoom Text Size", min_value=10, max_value=50, value=st.session_state.global_zoom, key="zoom_step2", on_change=sync_zoom, args=("zoom_step2",))
            
            # Use the global final_search_query state variable
            if st.session_state.get('final_search_query'):
                mode_enh = st.toggle("✏️ Edit Query Manually", value=st.session_state.is_editing_enhanced)
                st.session_state.is_editing_enhanced = mode_enh
                
                if st.session_state.is_editing_enhanced:
                    edited = st.text_area("Edit Search Query", st.session_state.final_search_query, height=400, label_visibility="collapsed")
                    if st.button("Save Query Edits", type="primary"):
                        st.session_state.final_search_query = edited
                        st.toast("Edits saved!", icon="✅")
                        st.session_state.is_editing_enhanced = False
                        st.rerun()
                else:
                    st.markdown(f"<div style='font-size: {st.session_state.global_zoom}px;'>{st.session_state.final_search_query}</div>", unsafe_allow_html=True)

# Call the function to render it
render_query_enhancement_step(manager=ai_manager, default_prompt="RAG_query")

# ---------------------------------------------------------
# STEP 3: ADVANCED RETRIEVAL & INTERACTIVE CURATION
# ---------------------------------------------------------
st.header("Step 3: Advanced Retrieval & Context Curation")
st.markdown("Fine-tune the exact mechanics of the vector search, rerank the outputs, and curate the exact citations.")

# 1. HOIST THE FRAGMENT OUTSIDE OF ALL LOOPS
@st.fragment
def render_chunk_ui(doc, score, meta, citation, filename, c_idx, use_llm_rerank):
    # Generate a universally unique ID based on the chunk's actual text content
    unique_hash = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()[:8]
    txt_key = f"chunk_txt_{unique_hash}_{c_idx}"
    chk_key = f"chk_apprv_{unique_hash}_{c_idx}"
    
    col_chunk, col_meta = st.columns([3, 1])
    
    with col_chunk:
        score_label = "LLM Score" if use_llm_rerank else "Vector Relevance"
        st.caption(f"**Chunk #{c_idx + 1}** | {score_label}: `{score:.4f}`")
        
        edited_chunk = st.text_area(
            "Edit this chunk before final context insertion:", 
            value=doc.page_content, 
            height=150, 
            key=txt_key,
            label_visibility="collapsed"
        )
        
        is_approved = st.checkbox(f"✅ Approve Chunk #{c_idx + 1} for Final Synthesis", key=chk_key)
        
    with col_meta:
        st.info("**Extracted Citation:**")
        st.markdown(citation)
        with st.expander("View Raw metadata.json"):
            st.json(meta)

    # Save to State if Approved
    if is_approved:
        st.session_state.curated_contexts[c_idx] = {
            "text": edited_chunk,
            "citation": citation,
            "source": filename
        }
    else:
        st.session_state.curated_contexts.pop(c_idx, None)


# 2. MAIN LOGIC
if 'final_search_query' not in st.session_state or not st.session_state.final_search_query:
    st.info("⚠️ Please complete Step 2 to generate a final search query.")
elif 'vector_db' not in st.session_state:
    st.error("⚠️ Vector Database not found. Please complete Step 1.")
else:
    # --- ADVANCED RETRIEVAL PARAMETERS UI ---
    with st.expander("⚙️ Advanced Retrieval Parameters", expanded=True):
        st.info("Adjusting these parameters alters how the pipeline queries the DB and post-processes the chunks.")
        
        col_ret1, col_ret2, col_ret3 = st.columns(3)
        
        with col_ret1:
            st.markdown("**Base Search Config**")
            top_k = st.number_input("Initial Retrieval Top-K", min_value=1, max_value=50, value=10, help="How many raw chunks to pull from the DB.")
            sim_threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05, help="Minimum relevance score (0-1) to be considered.")
            alpha_weight = st.slider("Hybrid Alpha (α)", min_value=0.0, max_value=1.0, value=1.0, step=0.1, help="0.0 = Pure Keyword | 1.0 = Pure Semantic.")
            
        with col_ret2:
            st.markdown("**Query Transformations**")
            use_hyde = st.toggle("Enable HyDE", value=False, help="Hypothetical Document Embeddings.")
            use_step_back = st.toggle("Enable Step-Back", value=False, help="Prompts the LLM to generate a broader version of the query.")
            
        with col_ret3:
            st.markdown("**Post-Processing / Reranking**")
            use_llm_rerank = st.toggle("Enable LLM Reranking", value=False)
            if use_llm_rerank:
                rerank_top_n = st.number_input("Rerank Top-N", min_value=1, max_value=top_k, value=5)
                available_models = ai_manager.get_models()
                default_models = ["No models found"] if not available_models else available_models
                rerank_idx = default_models.index("granite4:7b-a1b-h") if "granite4:7b-a1b-h" in default_models else 0
                rerank_model = st.selectbox("LLM for Reranking", default_models, index=rerank_idx, key="rerank_model_sel")
            else:
                rerank_top_n = top_k
                rerank_model = None

    # --- EXECUTE PIPELINE ---
    if st.button("🔍 Execute Advanced Search", type="primary"):
        search_query = st.session_state.final_search_query
        with st.status("Executing Retrieval Pipeline...", expanded=True) as ret_status:
            try:
                st.write(f"📡 Querying VectorDB for Top {top_k} chunks...")
                raw_results = st.session_state.vector_db.similarity_search_with_relevance_scores(search_query, k=top_k)
                
                st.write(f"⚖️ Applying Similarity Threshold (>= {sim_threshold})...")
                filtered_results = [(doc, score) for doc, score in raw_results if score >= sim_threshold]
                st.write(f"📉 *Dropped {len(raw_results) - len(filtered_results)} chunks below threshold.*")
                
                if use_llm_rerank and filtered_results:
                    st.write(f"🧠 Passing {len(filtered_results)} chunks to `{rerank_model}` for reranking...")
                    reranked_buffer = []
                    for doc, _ in filtered_results:
                        score_prompt = f"Given the query: '{search_query}', score relevance strictly from 1 to 10. Reply ONLY with the number.\n\nText: {doc.page_content}"
                        try:
                            llm_score_str = ai_manager.generate_sync(score_prompt, "You are a relevance grader. Reply ONLY with a single integer from 1 to 10.", rerank_model, 0.1, 10).strip()
                            match = re.search(r'\d+', llm_score_str)
                            llm_score = int(match.group()) if match else 0
                        except Exception:
                            llm_score = 0
                        reranked_buffer.append({"doc": doc, "llm_score": llm_score})
                    
                    reranked_buffer.sort(key=lambda x: x['llm_score'], reverse=True)
                    final_results = [(item["doc"], item["llm_score"]) for item in reranked_buffer[:rerank_top_n]]
                    st.write(f"🏆 Reranking complete. Kept top {rerank_top_n} chunks.")
                else:
                    final_results = filtered_results[:rerank_top_n]
                
                st.session_state.retrieval_results = final_results
                ret_status.update(label=f"Complete! Found {len(final_results)} highly relevant chunks.", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"Search failed: {e}")
                ret_status.update(label="Pipeline Failed", state="error")

    # --- RESULTS & INTERACTIVE CURATION UI ---
    if 'retrieval_results' in st.session_state and st.session_state.retrieval_results:
        st.divider()
        st.subheader("📚 Curate Retrieved Context & Citations")
        
        if 'curated_contexts' not in st.session_state:
            st.session_state.curated_contexts = {}

        grouped_docs = {}
        for doc, score in st.session_state.retrieval_results:
            src = doc.metadata.get('source', 'Unknown')
            if src not in grouped_docs:
                grouped_docs[src] = []
            grouped_docs[src].append((doc, score))

        chunk_index = 0
        
        for source_path, chunks_data in grouped_docs.items():
            filename = os.path.basename(source_path)
            dir_name = os.path.dirname(source_path)
            json_path = os.path.join(dir_name, "metadata.json")
            real_metadata = {}
            
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as jf:
                        file_meta = json.load(jf)
                        if isinstance(file_meta, dict) and filename in file_meta:
                            real_metadata = file_meta[filename]
                        elif isinstance(file_meta, list):
                            for item in file_meta:
                                if item.get('source') == filename or item.get('file') == filename:
                                    real_metadata = item
                                    break
                        else:
                            real_metadata = file_meta
                except Exception as e:
                    st.warning(f"Found metadata.json in {dir_name} but couldn't read it: {e}")
            else:
                st.warning(f"No metadata.json found in {dir_name}. Citation info may be limited.")

            st.markdown(f"### 📄 Source: `{filename}`")
            
            with st.expander(f"👁️ View Entire Document ({len(chunks_data)} retrieved chunks highlighted)"):
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        full_text = f.read()
                        
                    highlighted_text = full_text
                    for c_doc, _ in chunks_data:
                        safe_chunk = re.escape(c_doc.page_content)
                        highlighted_text = re.sub(
                            f"({safe_chunk})", 
                            r"<mark style='background-color: rgba(255, 235, 59, 0.5); color: inherit; padding: 2px; border-radius: 3px;'>\1</mark>", 
                            highlighted_text
                        )
                    st.markdown(f"<div style='font-size: {st.session_state.get('global_zoom', 16)}px; height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ccc;'>{highlighted_text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Could not load or highlight original file: {e}")

            # CLEAN LOOP: Only calculating citations and calling the fragment. No duplicate UI code.
            for doc, score in chunks_data:
                doi = real_metadata.get('doi') or real_metadata.get('DOI')
                url = real_metadata.get('url') or real_metadata.get('URL')
                citation_text = ""
                
                if doi:
                    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
                    try:
                        headers = {"Accept": "text/x-bibliography; style=apa"}
                        response = requests.get(f"https://doi.org/{clean_doi}", headers=headers, timeout=5)
                        if response.status_code == 200:
                            citation_text = response.text.strip()
                        else:
                            citation_text = f"DOI Found: {doi} (API timeout. Please use Scribbr manually)"
                    except Exception:
                        citation_text = f"DOI Found: {doi} (Fetch failed)"
                elif url:
                    citation_text = f"URL Found: {url}\n\n[🔗 Generate Citation via Scribbr](https://www.scribbr.com/citation/generator/)"
                else:
                    citation_text = f"Local File: {filename} (No DOI or URL found in metadata.json)"

                # CALL FRAGMENT (No duplicate UI elements!)
                render_chunk_ui(doc, score, real_metadata, citation_text, filename, chunk_index, use_llm_rerank)
                chunk_index += 1

        if st.session_state.curated_contexts:
            st.success(f"🎉 **Ready for Generation:** You have curated {len(st.session_state.curated_contexts)} chunks of context.")