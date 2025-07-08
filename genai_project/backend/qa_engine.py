# backend/qa_engine.py

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

def get_chunks(text, chunk_size=800, chunk_overlap=100):
    # Step 1: Split by paragraphs first
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # Step 2: Convert to Document objects with metadata
    docs = []
    for idx, para in enumerate(paragraphs, 1):  # Start at paragraph 1
        doc = Document(page_content=para, metadata={"paragraph_number": idx})
        docs.append(doc)

    # Step 3: Use RecursiveCharacterTextSplitter with metadata preserved
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunked_docs = splitter.split_documents(docs)

    return chunked_docs

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embedding=embeddings)

def get_qa_chain(vectorstore):
    local_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=256)
    llm = HuggingFacePipeline(pipeline=local_pipeline)
    return RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

def answer_question(question, chain, return_source=False):
    result = chain({"query": question}, return_only_outputs=True)

    if return_source:
        docs = chain.retriever.get_relevant_documents(question)
        if docs:
            top_doc = docs[0]
            para_num = top_doc.metadata.get("paragraph_number", "Unknown")
            return {
                "answer": result["result"],
                "paragraph": f"Paragraph {para_num}: {top_doc.page_content[:150]}"
            }

    return result["result"]

