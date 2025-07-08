# 📄 GenAI Document Assistant — Data Science Internship Assessment

A full-stack **GenAI-powered assistant** that understands documents. Upload any `.PDF` or `.TXT` file, and the system can:

- 📝 Summarize the content  
- ❓ Answer your questions  
- 🚀 Automatically generate practice questions  
- 📊 Evaluate your answer and provide intelligent feedback

Built using **LangChain**, **Flan-T5**, **Django**, and **Streamlit**.

---

## 🧠 Features

| Feature              | Description                                         |
|----------------------|-----------------------------------------------------|
| 📤 Upload Document   | Upload `.pdf` or `.txt` files                       |
| 📝 Summary           | Generate a short, meaningful summary                |
| ❓ Ask a Question     | Ask anything from the uploaded document             |
| 🚀 Challenge Mode     | Auto-generate a practice question from content      |
| 📊 Feedback          | Submit answers and get performance feedback         |
---

## 🛠 Tech Stack

| Layer       | Tools                                           |
|-------------|-------------------------------------------------|
| ⚙️ Backend   | Django, Django REST Framework, LangChain        |
| 🧠 LLM       | Flan-T5 (`text2text-generation` via HuggingFace)|
| 🔍 Search    | FAISS vector store + Sentence Embeddings        |
| 📤 Frontend  | Streamlit                                       |
| 📚 NLP Utils | PyMuPDF (PDF parsing), spaCy, NLTK, Transformers|

---

## 📁 Project Structure

-genai_project/
- │
- ├── assistant/ # Django app (API layer)
- │ ├── views.py
- │ ├── urls.py
- │ └── models.py
- │
- ├── backend/ # Core LangChain + QA/Summarizer logic
- │ ├── qa_engine.py # Custom heading-aware QA logic
- │ ├── summarizer.py # Custom summarizer with heading-aware rules
- │ ├── challenge.py # Auto-question generator logic
- │
- ├── genai_project/ # Django settings and routing
- │ ├── settings.py
- │ ├── urls.py
- │ └── ...
- │
- ├── app.py # Streamlit frontend
- ├── temp/ # Stores uploaded files (optional)
- ├── requirements.txt
- └── README.md

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/genai-doc-assistant.git
cd genai-doc-assistant
```
### 2.Create a Virtual Environment and Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3.Run the Django Backend
```bash
cd genai_project
python manage.py migrate
python manage.py runserver
```
### 4.Run the Streamlit Frontend
Open a new terminal in the root project folder and run:
```bash
streamlit run app.py
```
---

## ⚠️ Known Limitations

While the GenAI Document Assistant performs well on structured documents, it still has a few areas for improvement:

- 🔄 **Answer Evaluation:** The feedback logic for long or descriptive answers may not always align with human reasoning, especially on subjective content.
- 🧠 **Challenge Question Depth:** Currently, challenge-mode questions are basic and rely on surface-level sentence structure.
- 📄 **Model Behavior:** The Flan-T5 model sometimes generates repetitive answers or hallucinations, especially when context is insufficient.
- 🧪 **Offline Accuracy:** Offline QA logic (lemmatization, POS tagging) may miss some multi-word or embedded concepts in technical docs.

These limitations are being tracked for improvement via better prompt engineering, offline chunk filtering, and experimenting with different LLMs or hybrid retrieval pipelines.

---
