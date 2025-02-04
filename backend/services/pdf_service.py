# services/pdf_service.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sklearn.metrics.pairwise import cosine_similarity

def load_and_process_pdf(pdf_path, chunk_size=500, overlap=50, page_limit=50):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # Limit the number of pages processed
    docs = docs[:page_limit]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap, separators=["\n\n", "\n", " "])
    chunks = text_splitter.split_documents(docs)
    vectors = FAISS.from_documents(chunks, embeddings)
    return embeddings, vectors, chunks

def retrieve_relevant_docs(prompt, chunks, embeddings, top_k=10):
    query_embedding = embeddings.embed_query(prompt)
    chunk_embeddings = [embeddings.embed_query(chunk.page_content) for chunk in chunks]
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
    
    # Limit the number of top-k relevant documents
    top_indices = similarities.argsort()[-top_k:][::-1]
    relevant_docs = [chunks[i] for i in top_indices]
    
    return relevant_docs