# 🔍 GitASK – Your AI-Powered GitHub Documentation Assistant

GitASK is an intelligent, locally-hosted assistant that lets you **ask questions about any public GitHub repository** — using powerful **LLMs**, **embeddings**, and **retrieval-based querying**.

Just paste a GitHub repo URL, and GitASK will:
- Clone the repo into a temporary folder
- Index key files like `README.md`, Python code, and documentation
- Use **ChromaDB** + **Ollama** (LLaMA3/other models) to build vector embeddings
- Let you **chat with the repo** using natural language

Whether you're onboarding a project, exploring an unfamiliar codebase, or building developer tools — just **GitASK it**.

---

## 🧠 How It Works

1. **Ingest**:
   - GitASK clones the GitHub repo into a temporary folder
   - Parses all relevant `.md`, `.py`, `.txt`, `.js` and `.json` files

2. **Embed**:
   - Text chunks are embedded using `nomic-embed-text` (via Ollama)
   - Embeddings are stored in a **local ChromaDB**

3. **Query**:
   - You type a question (e.g., "What does the `predict()` function do?")
   - GitASK retrieves relevant document chunks and feeds them into an LLM
   - You get a concise, context-aware answer — just like ChatGPT for repos!

---

## 🚀 Features

- 🧠 Uses **local LLMs via Ollama** — no API keys or internet required
- ⚡️ Fast embeddings with **nomic-embed-text**
- 🧰 Based on **ChromaDB** for lightweight vector storage
- 🧾 Summarizes README, function docs, usage examples
- 🔐 Runs entirely on your machine — secure & private
- 🌐 Can be shared publicly via `cloudflared`

---

## 📦 Requirements

- Python 3.9+
- [Ollama](https://ollama.com) (installed and running)
- Git
- pip

---

## 🛠️ Installation & Usage

### 1️⃣ Clone the Repo
```markdown
git clone https://github.com/Unnathi-baskar/GitASK---AI-Powered-GitHub-Documentation-Assistant
cd gitask
``` 
2️⃣ Set Up a Virtual Environment (recommended)
```markdown
python3 -m venv venv
source venv/bin/activate
```
3️⃣ Install Dependencies
```markdown
pip install -r requirements.txt
```
4️⃣ Start Ollama in a separate terminal
```markdown
ollama run llama3
ollama run nomic-embed-text
```
5️⃣ Run the App
```markdown
streamlit run app.py
```

Built with ❤️ using Streamlit, Ollama, and ChromaDB.
