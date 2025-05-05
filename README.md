# **YouTube Video Q&A with RAG**  

🚀 **A Retrieval-Augmented Generation (RAG) system that lets you ask questions about any YouTube video and get accurate, context-aware answers.**  

---

## **📌 Features**  

✅ **Transcript Extraction** – Automatically fetches YouTube video captions.  
✅ **Smart Chunking** – Splits long transcripts into meaningful segments.  
✅ **Semantic Search** – Uses **HuggingFace embeddings** + **FAISS vector DB** for fast retrieval.  
✅ **AI-Powered Answers** – Generates responses using **Cohere’s LLM** (or local models like Mistral).  
✅ **Interactive Chat UI** – Built with **Streamlit** for a seamless user experience.  
✅ **Persistent Storage** – Saves processed videos locally for faster reloads.  

---

## **⚙️ Tech Stack**  

| Component | Technology |  
|-----------|------------|  
| **Backend** | FastAPI, LangChain |  
| **Vector DB** | FAISS (Facebook AI Similarity Search) |  
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |  
| **LLM** | Cohere `command` (or Ollama for local models) |  
| **Frontend** | Streamlit |  
| **Transcript Fetching** | `youtube-transcript-api` |  

---

## **🚀 Quick Start**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/youtube-rag.git
cd youtube-rag
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Set Up API Keys**  
Create a `.env` file:  
```env
COHERE_API_KEY="your_cohere_key"  # Optional (if using Cohere)
HUGGINGFACEHUB_API_TOKEN="your_hf_token"  # Optional (if using HF models)
```

### **4. Run the Backend (FastAPI)**  
```bash
uvicorn backend.main:app --reload
```

### **5. Run the Frontend (Streamlit)**  
```bash
streamlit run frontend/app.py
```
📌 Open `http://localhost:8501` in your browser.  

---

## **🛠️ How It Works**  

1. **User Input** → Enter a YouTube video ID (e.g., `dQw4w9WgXcQ`).  
2. **Transcript Processing** → Fetches captions, splits into chunks, and stores embeddings in FAISS.  
3. **Question Handling** → Searches for relevant chunks and generates an answer using an LLM.  
4. **Response** → Displays a natural-language answer with source context.  

---

## **🔍 Example Queries**  

❓ *"What is the main topic of this video?"*  
❓ *"Explain the key points about [topic]."*  
❓ *"Does this video mention [specific detail]?"*  

---

## **📂 Project Structure**  

```plaintext
youtube-rag/  
├── backend/  
│   ├── main.py           # FastAPI server  
│   ├── rag_processor.py  # Core RAG logic  
│   └── requirements.txt  
├── frontend/  
│   ├── app.py            # Streamlit UI  
│   └── requirements.txt  
├── .env                  # API keys  
└── README.md  
```

---

## **📌 Future Improvements**  

🔹 **Add Timestamp References** – Link answers to exact video timestamps.  
🔹 **Support Local LLMs** – Integrate Ollama for offline usage.  
🔹 **Multilingual Support** – Expand beyond English transcripts.  
🔹 **Deploy to Cloud** – Host on **Hugging Face Spaces** or **Streamlit Cloud**.  

---

## **📜 License**  
MIT License - Free for personal and academic use.  

---

## **💡 Contribute**  
Found a bug? Want to improve something? Open an **issue** or submit a **PR**!  

📧 **Contact**: [gautam2002gkp@gmail.com]  

--- 
