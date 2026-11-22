# AI Assistant

**Modular desktop AI assistant** built with Python — modern GUI, persistent chat history, streaming responses, and secure environment-based configuration.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Personal-lightgrey)](#)

**Author:** [Amirhossein Bakhshi](https://github.com/Amirhosseinbakhshi2011)  
**Stack:** Python · CustomTkinter · OpenAI-compatible APIs

---

## Features

- Modern desktop UI with **CustomTkinter**
- Chat with OpenAI / OpenRouter and other compatible APIs
- **Streaming** responses
- Persistent chat history (local JSON)
- Robust error handling, timeouts, and offline awareness
- Secure configuration via `.env` (never commit secrets)
- Clean modular architecture ready for extensions (tools, agents, voice, …)

---

## Requirements

- Python **3.11+**
- API key from OpenAI or a compatible provider (e.g. OpenRouter)

---

## Quick start

```bash
git clone https://github.com/Amirhosseinbakhshi2011/AI.git
cd AI

python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set your API key

python main.py
```

---

## Project structure

```text
AI/
├── main.py              # Entry point
├── config/              # Settings & env loading
├── core/                # AI client, assistant logic, chat history
├── ui/                  # CustomTkinter main window
├── utils/               # Logging helpers
├── data/chats/          # Chat history (gitignored)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Configuration

Copy `.env.example` → `.env` and set at least:

```env
API_KEY=your_key_here
# Optional: base URL, model name, etc. (see .env.example)
```

Never commit real `.env` files.

---

## Roadmap

- [ ] Better conversation export / search
- [ ] Plugin-style tools (web search, code runner, …)
- [ ] Multi-model switcher in UI
- [ ] Optional local models support
- [ ] Unit tests for core modules

---

## Notes for contributors / reviewers

- `__pycache__/`, `.idea/`, `logs/`, and `data/chats/*.json` are ignored.
- If you still see them in the tree, they were committed before the ignore rules; they should not be added in new commits.

---

Built with Python and curiosity.  
**Amirhossein Bakhshi** · 16 · Iran → USA
