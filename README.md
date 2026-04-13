# YouLearn

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

YouLearn is a comprehensive AI-powered learning platform built with Streamlit that transforms educational content from YouTube videos and academic PDFs into structured, interactive learning materials. It combines Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) to create personalized learning experiences with note generation, quiz creation, and speed-reading capabilities.

## 🌟 Key Features

### 📺 YouTube Learning Pipeline
- **Transcript Processing**: Fetch and cache YouTube transcripts with automatic metadata extraction
- **Interactive Editing**: Timestamp-synchronized video playback with inline transcript editing
- **AI Enhancement**: Convert raw transcripts into structured Obsidian-style markdown notes
- **Quiz Generation**: Create adaptive multiple-choice quizzes from enhanced content
- **Speed Reading**: Built-in RSVP (Rapid Serial Visual Presentation) module for accelerated comprehension

### 📄 PDF Processing & Academic Integration
- **Zotero Integration**: Batch download and process PDFs from Zotero libraries
- **Advanced Parsing**: Multiple PDF-to-markdown conversion strategies (PyMuPDF4LLM, Docling)
- **Metadata Enrichment**: Automatic DOI lookup via Crossref API for academic papers
- **Image Extraction**: Preserve inline images and figures during conversion

### 🔍 Advanced RAG (Retrieval-Augmented Generation)
- **Vector Database**: ChromaDB integration with configurable chunking strategies
- **Semantic Search**: Multi-source content retrieval across documents
- **Flexible Embeddings**: Support for both cloud (Gemini) and local (Ollama) embedding models
- **Smart Indexing**: Incremental updates with metadata-aware deduplication

### 🤖 AI-Powered Enhancement
- **Multi-Provider LLM Support**: Google Gemini and Ollama integration
- **Customizable Prompts**: Persistent prompt templates for different content types
- **Streaming Generation**: Real-time content generation with adjustable parameters
- **No-Hallucination Guardrails**: Academic-focused prompts ensuring factual accuracy

## 🏗️ Architecture

```
YouLearn/
├── main.py                 # Multi-page Streamlit orchestrator
├── pages/
│   ├── youtube.py          # YouTube transcript pipeline
│   ├── pdf.py             # PDF processing & Zotero integration
│   └── advanced_rag.py    # Vector database configuration
├── AI_manager.py          # Unified LLM abstraction layer
├── functions.py           # Utility functions for data processing
├── shared_ui.py           # Reusable UI components
├── spreader.py            # Speed-reading RSVP module
├── system_prompts.json    # Persistent AI prompt templates
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Internet connection for API access
- API keys for transcript and LLM services

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Daedalo98/YouLearn.git
   cd YouLearn
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your API keys:
   ```ini
   # Required
   TRANSCRIPT_API_KEY=your_transcriptapi_key
   GEMINI_API_KEY=your_gemini_api_key

   # Optional (for Zotero integration)
   ZOTERO_LIB_ID=your_zotero_library_id
   ZOTERO_API_KEY=your_zotero_api_key
   ```

### Running the Application

```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your browser.

### Running with Docker

Build and run the app with Docker using the provided `Dockerfile` and `docker-compose.yml`.

1. Create or update `.env` with your API keys.
2. Build and start the container:

```bash
docker compose up --build
```

3. Open the app:

```text
http://localhost:8501
```

### Docker Notes

- The `Dockerfile` installs dependencies from `requirements.txt` and exposes Streamlit on port `8501`.
- `docker-compose.yml` mounts the repository and persistent storage directories:
  - `saved_pdfs`
  - `saved_transcripts`
  - `chroma_db`
- Environment variables are loaded from `.env`.

## 📖 Usage Guide

### YouTube Learning Pipeline

1. **Select YouTube Page** from the sidebar navigation
2. **Enter YouTube URL** (supports standard, shorts, and live videos)
3. **Fetch Transcript** - Automatically downloads and caches transcript data
4. **Edit Transcript** - Use the dual-pane interface to edit segments with timestamp sync
5. **Enhance Content** - Select a prompt template and generate structured notes
6. **Take Quiz** - Generate and answer multiple-choice questions
7. **Speed Read** - Use the Spreader module for accelerated reading

### PDF Processing Pipeline

1. **Navigate to PDF Page**
2. **Connect Zotero** (optional) - Provide library credentials for batch processing
3. **Upload PDFs** or process Zotero library
4. **Parse Documents** - Choose between PyMuPDF4LLM or Docling parsers
5. **Review Enhanced Markdown** - Edit and download structured content
6. **Generate Quizzes** - Create interactive assessments

### Advanced RAG Configuration

1. **Select RAG Page**
2. **Choose Data Source** - Point to a directory containing markdown files
3. **Configure Chunking** - Select splitting strategy and parameters
4. **Set Embedding Model** - Choose between Gemini or Ollama embeddings
5. **Build Vector Database** - Create or update ChromaDB index
6. **Query Content** - Perform semantic search across your knowledge base

## ⚙️ Configuration

### API Keys Setup

- **TRANSCRIPT_API_KEY**: Obtain from [transcriptapi.com](https://transcriptapi.com)
- **GEMINI_API_KEY**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **ZOTERO_API_KEY**: Generate in your [Zotero account settings](https://www.zotero.org/settings/keys)

### System Prompts

Customize `system_prompts.json` to define prompt templates:

```json
{
  "Obsidian_Default": "You are an expert knowledge manager...",
  "Academic_Note": "Process academic content into structured notes...",
  "Quiz_Generator": "Generate educational multiple-choice questions..."
}
```

### LLM Configuration

- **Primary**: Google Gemini (gemini-2.5-flash, gemini-2.5-pro)
- **Fallback**: Local Ollama instance (`http://localhost:11434`)
- **Embeddings**: Gemini embeddings or Ollama models

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **LangChain**: RAG pipeline orchestration
- **ChromaDB**: Vector database for semantic search
- **PyMuPDF4LLM**: PDF processing with image extraction
- **PyZotero**: Zotero library integration
- **YouTube Transcript API**: Video transcript fetching

### Data Storage
- **Transcripts**: `saved_transcripts/{video_id}.json`
- **PDFs**: `saved_pdfs/{doc_id}/` with metadata and images
- **Vector DB**: ChromaDB instances in `chroma_db/` directories
- **Prompts**: Persistent templates in `system_prompts.json`

### Performance Features
- **Caching**: Automatic caching of transcripts and metadata
- **Streaming**: Real-time LLM generation with progress indicators
- **Background Processing**: Asynchronous quiz generation
- **Smart Deduplication**: Metadata-aware vector database updates

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini](https://ai.google.dev/) and [Ollama](https://ollama.ai/)
- PDF processing via [PyMuPDF](https://pymupdf.readthedocs.io/)
- Vector search with [ChromaDB](https://www.trychroma.com/)

## 🐛 Troubleshooting

### Common Issues

**"Cannot fetch transcript"**
- Verify `TRANSCRIPT_API_KEY` is correct
- Check internet connection
- Ensure YouTube video has captions available

**"LLM connection failed"**
- For Gemini: Verify `GEMINI_API_KEY`
- For Ollama: Ensure Ollama is running locally
- Check API rate limits and quotas

**"Zotero connection error"**
- Verify library ID and API key
- Ensure Zotero library is publicly accessible or API key has correct permissions

**Performance Issues**
- Reduce chunk size in RAG configuration
- Use local Ollama for embeddings to reduce API calls
- Clear cache directories if storage is full

### Getting Help

- Check existing [Issues](https://github.com/Daedalo98/YouLearn/issues) on GitHub
- Create a new issue with detailed error logs
- Include your system information and configuration (without API keys)

---

**Transform your learning experience with AI-powered content enhancement and interactive discovery!** 🚀

