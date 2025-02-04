# controllers/process_controller.py

from flask import jsonify, request
from services.model_service import get_model_response
from services.evaluation_service import calculate_accuracy, calculate_bert_score, combined_word_matching, exact_word_matching, extract_unique_words
from services.pdf_service import load_and_process_pdf, retrieve_relevant_docs

def process_file():
    data = request.get_json()
    file_path = data.get('filePath')
    prompt = data.get('prompt')

    if not file_path or not prompt:
        return jsonify({'error': 'File path and prompt are required'}), 400

    context, output, error = get_model_response(file_path, prompt)
    
    if error:
        return jsonify({'error': f'Failed to process: {error}'}), 500
    
    # Calculate the accuracy 
    embeddings, vectors, chunks = load_and_process_pdf(file_path, chunk_size=500)
    relevent_docs = retrieve_relevant_docs(prompt, chunks, embeddings)
    reference_text = [doc.page_content for doc in relevent_docs]
    reference_text_combined = " ".join(reference_text)

    accuracy = calculate_accuracy(output, relevent_docs, embeddings)
    bert_score = calculate_bert_score(output, reference_text)

    # Calculate word matching
    word_matching_result = combined_word_matching(output, reference_text_combined)
    word_matching_result1 = exact_word_matching(output, reference_text_combined)
    
    matched_words_format = ", ".join(word_matching_result1[1])
    reference_words_format = ", ".join(word_matching_result["reference_words"])

    exact_match_normalized = word_matching_result['exact_match_percentage'] / 100
    fuzzy_match_normalized = word_matching_result['fuzzy_match_percentage'] / 100

    # Calculate the final score as a weighted average
    final_score = (
    (bert_score['f1'] * 0.7) +
    (exact_match_normalized * 0.15) +
    (fuzzy_match_normalized * 0.15)
    )

    # Extract unique words from chunks and LLM response
    unique_words_chunks = ", ".join(extract_unique_words(reference_text_combined))
    unique_words_llm = ", ".join(extract_unique_words(output))


    return jsonify({
        'context': context,
        'modelAnswer': output,
        # 'accuracy': accuracy,
        # 'bert_score': bert_score,
        # 'word_matching': word_matching_result,
        'final_score': final_score,
        # 'matched_words': matched_words_format, # List of exactly matched words
        # 'reference_words': reference_words_format, # List of corresponding reference words
        'unique_words_chunks': unique_words_chunks,  # Unique words from chunks
        'unique_words_llm': unique_words_llm  # Unique words from LLM response

    }), 200