# YouLearn

## 🚀 Project Overview

YouLearn is a Streamlit-based app for transforming YouTube video transcripts into structured notes and quiz questions using LLMs (Google Gemini or local Ollama via API). It supports:

- Fetching and caching YouTube transcripts (via `transcriptapi.com`)
- Playback with timestamp synchronized editing
- Transcript editing + markdown preview
- LLM-based 1) Obsidian-style note generation and 2) quiz question generation
- Persistent prompt templates stored in `system_prompts.json`

## 📁 Key Files

- `app.py`: Main Streamlit app UI + app flow
- `functions.py`: transcript fetch/save/format + prompts + quiz context + helpers
- `AI_manager.py`: AI provider client wrapper (Gemini + Ollama fallback)
- `system_prompts.json`: prompt definitions for note and quiz generation
- `.env.example`: required API keys (uname + track configs)
- `saved_transcripts/`: local cached transcripts and enhancements

## ⚙️ Prerequisites

- Python 3.10+
- `pip` and optional `virtualenv`
- Internet access for YouTube + transcript API
- LLM provider credentials:
  - `TRANSCRIPT_API_KEY` from https://transcriptapi.com
  - `GEMINI_API_KEY` for Google GenAI (or local Ollama instance at `http://localhost:11434`)

## 🛠️ Setup steps

1. Clone repository (if not already):

```bash
git clone https://github.com/Daedalo98/YouLearn
cd YouLearn
```

2. Create virtual env and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Copy environment template:

```bash
cp .env.example .env
```

4. Edit `.env` with your keys:

```ini
TRANSCRIPT_API_KEY=your_actual_transcript_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
```

If you don’t have Gemini, run Ollama locally and set model names in the app UI.

## ▶️ Running the app

```bash
streamlit run app.py
```

Then open the local URL, usually `http://localhost:8501`.

## 🧩 Usage workflow

1. In the sidebar, paste a YouTube URL (standard, short, shorts, or live link).  
2. Click `Fetch & Process Transcript`. This stores in `saved_transcripts/{video_id}.json`.  
3. Edit transcript segments inline, adjust time anchor from 2-column timeline, save auto-updates cache.  
4. Choose a prompt from `system_prompts.json` and adjust text in the prompt editor.  
5. Click `Generate Note` for Obsidian-style summary from LLM.  
6. Use quiz mode in the app to generate multiple-choice questions from notes and the prompt.

## 🗂️ `system_prompts.json` format

```json
{
    "Obsidian_Default": "You are an expert knowledge manager. Process the provided YouTube video metadata and transcript into a highly structured, Obsidian-style Markdown note.\n\nRequirements:\n0. Include a title at the top using the video title (# video title).\n1. Include a YAML frontmatter block with: tags (e.g., #tag1, #tag2), aliases, author, date, and source url.\n2. Create a brief 'Summary' section.\n3. Create a 'Key Insights' section using bullet points.\n4. Format the main concepts under clear header sections.\n5. Include a 'Related / Connections' section at the bottom for internal wiki linking (e.g., [[Concept Name]]).\n6. Do NOT hallucinate. Rely strictly on the provided transcript.",
    "Quiz_Generator": "You are an adaptive expert educator. Based on the provided notes and the history of previous questions, generate EXACTLY ONE new multiple-choice question.\nEnsure the question is different from previous ones. If the user got previous questions wrong, focus on those concepts.\nYou MUST output ONLY a valid JSON object. No markdown, no arrays, no conversational text.\nFormat strictly like this:\n{\n  \"question\": \"What is the main topic?\",\n  \"options\": [\"A\", \"B\", \"C\", \"D\"],\n  \"answer\": \"A\",\n  \"explanation\": \"Because the notes state...\"\n}"
}
```

## 🧪 Validation checks

- `test whether .env keys are set`: The app warns when missing.
- `TRANSCRIPT_API_KEY` used for transcript API.
- `GEMINI_API_KEY` used by `AI_manager.Manager` for Google GenAI.

## 🛡️ Common issues

- `video_id` mismatch / invalid YouTube URL: only well-formed 11-char IDs resolve.
- `Cannot connect to Ollama` if local model server unavailable.
- `JSON parse errors in system_prompts.json`: ensure valid JSON with `"` and no trailing commas.

## 💡 Enhancements

- Add logging middleware to persist app events
- Support batch transcript export `.md` or `.csv`
- Add auth and user settings for persistent prompt stores

---

**Note:** This README is generated from existing project code; adjust links and example keys for your deployment environment.

