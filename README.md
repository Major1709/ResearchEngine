# ResearchEngine
🧠 AI-Powered Thesis Search Engine
🎯 Project Goal
This project aims to build an AI-assisted search engine for academic theses and dissertations. Users can enter natural language queries (e.g., “Theses about the impact of AI in education”) and receive context-aware, relevant results, powered by LLMs.

🧰 Technologies
LLM (Large Language Model) – Understands user queries and thesis content semantically.

FastAPI – Backend API for indexing, search, and interaction with the LLM.

Python – Used for text processing, embedding, and model integration.

Next.js – Frontend for a fast, interactive search experience.

🔍 Key Features
🔎 Semantic Search – Finds relevant theses by meaning, not just keywords.

🧠 AI Summaries – Generates short descriptions of each result.

🗂️ Filters – Search by author, year, or discipline.

💬 Conversational UI – Ask follow-up questions in a chat-like interface.

📥 Auto Indexing – New PDFs are automatically extracted and indexed.

🔗 Workflow
Indexing: PDF text is extracted, vectorized, and stored.

Query: User submits a question via the Next.js frontend.

Search: FastAPI + LLM interpret and match the query.

Results: Displayed with highlights and smart filters.
