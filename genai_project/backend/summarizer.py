# backend/summarizer.py

from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def get_chunks(text, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents([Document(page_content=text)])

def generate_summary(text):
    summarizer = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=256)
    llm = HuggingFacePipeline(pipeline=summarizer)
    docs = get_chunks(text)
    chain = load_summarize_chain(llm=llm, chain_type="stuff")
    return chain.run(docs)
