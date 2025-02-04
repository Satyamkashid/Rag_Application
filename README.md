# RAG (Retrieval-Augmented Generation) Application

**This project demonstrates the power of Retrieval-Augmented Generation (RAG), combining the capabilities of Flask, React, FAISS, and Pretrained Language Models (LLMs) to create an intelligent document retrieval and response generation system. The application allows users to upload a PDF, generate meaningful responses to prompts, and evaluate the generated response using multiple metrics.**

## Key Features
1. PDF Parsing: Extracts text from uploaded PDF documents.
2. Chunking: Splits the PDF text into manageable chunks for better retrieval.
3. FAISS Integration: Uses FAISS for efficient storage and retrieval of document embeddings.
4. LLM Response Generation: Uses a language model to generate answers based on a given prompt.
5. Evaluation Metrics: The response is evaluated using:
        1. BERTScore: Measures semantic similarity between the generated response and reference text.
        2. Exact Word Matching: Compares exact words between the generated response and relevant chunks.
        3. Fuzzy Word Matching: Finds words that are similar but not exactly the same.
6. Word Extraction: Extracts unique words from both the document and the generated response for better understanding.

## How It Works
This application is designed to perform the following steps:

1. Upload a PDF: Users upload a PDF document from which the system will extract relevant content.
2. Enter a Prompt: Users provide a prompt (e.g., a question) related to the content of the document.
3. Chunking and Embedding: The document is split into chunks and embedded using a vectorization model.
4. Retrieving Relevant Chunks: The most relevant chunks are retrieved using FAISS.
5. Response Generation: A pre-trained language model (LLM) generates a response based on the relevant document chunks.
6. Evaluation: The response is evaluated using:
        BERTScore to measure similarity with reference text.
        Exact and Fuzzy Word Matching to assess how well the response matches with the document chunks.

## Project Structure
The project is divided into two main parts:

### 1. Backend (Flask API)
The backend of the application is built using Flask, and it exposes an API for interacting with the model. It handles file uploads, text extraction, chunking, and the response generation pipeline.

1. app.py: Main entry point for the Flask application.
2. services: Contains core logic for loading PDFs, embedding content, evaluating responses, etc.
3. controllers: Manages incoming API requests and triggers the relevant services.

### 2. Frontend (React)
The frontend is built using React, providing a user-friendly interface to upload files, enter prompts, and view the results.

1. App.js: The main React component managing the application’s UI.
2. components: Contains React components for uploading files, displaying results, etc.
3. api: Handles HTTP requests to the Flask backend.

## Getting Started
Follow the steps below to set up and run the project locally.

### Prerequisites
1. Python 3.x: Ensure you have Python 3.x installed on your machine.
2. Node.js: Required for the React frontend.
3. FAISS: A library for efficient similarity search, which is used for fast retrieval of document chunks.
Other dependencies: Python packages like bert_score, sklearn, and rapidfuzz for evaluation.

### Installation Steps
1. Clone the Repository:

git clone https://github.com/Satyamkashid/Rag_Application.git
cd Rag_Application

2. Backend Setup:

Navigate to the backend/ directory.
Install Python dependencies:

pip install -r requirements.txt

Run the Flask server:

python app.py

**The backend will be accessible at http://127.0.0.1:5000/**

3. Frontend Setup:

Navigate to the frontend/ directory.
Install Node.js dependencies

npm install

Start the React app

npm start

The frontend will be available at http://localhost:3000/.

## Usage
1. Upload a PDF: Once the backend and frontend are set up, go to the frontend UI and upload a PDF document.
2. Enter a Prompt: After the document is uploaded, enter a question or prompt related to the PDF content. For example, "What is the Turing Test?"
3. Get Response: The system processes the document, generates a response, and displays the results, including the generated answer and evaluation metrics.
4. Evaluate Response: The system will show how well the response matches the document using:
        1. BERTScore
        2. Exact and Fuzzy Word Matching

## API Endpoints

### POST /process_file
This endpoint processes the PDF and generates a response based on the given prompt.

Request Body:
{
  "filePath": "path_to_pdf_file",
  "prompt": "What is the Turing test?"
}

Response:
{
  "context": "Relevant chunks from the PDF.",
  "modelAnswer": "Generated response from the model.",
  "final_score": 85.6,
  "unique_words_chunks": "list of unique words from chunks",
  "unique_words_llm": "list of unique words from model response"
}

### Error Handling
If required fields (e.g., filePath, prompt) are missing, the API will respond with a 400 error.

In case of failure, the server will return an appropriate error message with a 500 status.

## Evaluation Metrics

### BERTScore

BERTScore is used to evaluate how well the generated response matches the reference text in terms of precision, recall, and F1 score. It computes these metrics by comparing the embeddings of the response and the reference text.

### Exact Word Matching

This metric calculates the percentage of words that are exactly the same in both the generated response and the reference document.

### Fuzzy Word Matching

Fuzzy word matching compares words in the generated response to reference words using similarity metrics (e.g., Levenshtein distance) to account for minor typos or variations in wording.

### Word Extraction

Unique words from both the chunks and the LLM-generated response are extracted to provide insights into the content's uniqueness.

### Contributing

Feel free to fork the repository, improve the project, and submit pull requests. Here are some ways you can contribute:
1. Improve documentation.
2. Enhance the evaluation metrics.
3. Add new features like support for other document formats.
4. Fix bugs or improve performance.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Enhanced Sections:
1. Project Structure: Added more details about both backend and frontend parts.
2. Evaluation Metrics: A deeper explanation of the evaluation methods and their importance.
3. API Error Handling: Mentioned how the API will respond in case of errors.