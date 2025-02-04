# services/model_service.py

import logging
from langchain_groq import ChatGroq
from services.pdf_service import load_and_process_pdf, retrieve_relevant_docs
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_model_response(file_path, prompt):
    """Centralized function to process file and get model response"""
    try:
        # Process the file
        embeddings, vectors, chunks = load_and_process_pdf(file_path, chunk_size=500)
        relevant_docs = retrieve_relevant_docs(prompt, chunks, embeddings)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        # Get model's response
        second_model = ChatGroq(groq_api_key=GROQ_API_KEY, model="Llama-3.3-70b-Versatile")
        input_for_model = f"""
        Based on the following context from a document, provide a clear and structured response.
        Your response should:
        1. Give the answer in details.
        2. Be well-organized with clear sections (Introduction, Body, Conclusion).
        3. Use precise and unambiguous language.
        4. Highlight key points from the context.
        5. Avoid adding information not present in the context.

        Context:\n{context}

        Question: {prompt}

        Provide a structured response using ONLY information from the above context:"""

        output = second_model.invoke(input_for_model).content
        
        return context, output, None
    except Exception as e:
        logging.error(f"Error in get_model_response: {str(e)}")
        return None, None, str(e)