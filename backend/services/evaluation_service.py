# services/evaluation_service.py

from bert_score import score
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz

def calculate_accuracy(llm_response, chunks, embeddings):
    # Embed the LLM response
    llm_embedding = embeddings.embed_query(llm_response)
    
    # Embed each chunk
    chunk_embeddings = [embeddings.embed_query(chunk.page_content) for chunk in chunks]
    
    # Calculate cosine similarity between LLM response and each chunk
    similarities = cosine_similarity([llm_embedding], chunk_embeddings)[0]
    
    # Average similarity score
    average_similarity = sum(similarities) / len(similarities)
    
    # Normalize to 0-100 scale
    accuracy = (average_similarity + 1) * 50
    
    return accuracy

def calculate_bert_score(model_response, reference_texts):
    """
    Calculate BERTScore for the model's response compared to reference texts.
    """
    # Combine reference texts into a single string (or keep them as a list)
    reference_texts_combined = " ".join(reference_texts)
    
    # Compute BERTScore
    P, R, F1 = score([model_response], [reference_texts_combined], lang="en", verbose=True)
    
    return {
        "precision": P.mean().item(),
        "recall": R.mean().item(),
        "f1": F1.mean().item()
    }

def exact_word_matching(response, reference_text):
    """
    Calculate the percentage of words in the response that exactly match the reference text
    and return the list of matched words and corresponding reference words.
    
    Args:
        response (str): The model's response.
        reference_text (str): The reference text (chunks).
    
    Returns:
        tuple: (percentage of exact matches, list of matched words, list of reference words)
    """
    # Tokenize the response and reference text into words
    response_words = response.lower().split()
    reference_words = reference_text.lower().split()
    
    # Find exact matches and corresponding reference words
    matched_words = []
    reference_matches = []
    for word in response_words:
        if word in reference_words:
            matched_words.append(word)
            reference_matches.append(word)
    
    # Calculate percentage of matching words
    if len(response_words) == 0:
        return 0.0, [], []
    match_percentage = (len(matched_words) / len(response_words)) * 100
    
    return match_percentage, matched_words, reference_matches


def fuzzy_word_matching(response, reference_text, threshold=80):
    """
    Calculate the percentage of words in the response that are similar to the reference text.
    """
    response_words = response.lower().split()
    reference_words = reference_text.lower().split()
    
    match_count = 0
    for word in response_words:
        for ref_word in reference_words:
            if fuzz.ratio(word, ref_word) >= threshold:
                match_count += 1
                break
    
    if len(response_words) == 0:
        return 0.0
    return (match_count / len(response_words)) * 100

def combined_word_matching(response, reference_text, fuzzy_threshold=80):
    """
    Calculate the percentage of words in the response that match the reference text
    using both exact and fuzzy matching, and return the list of exactly matched words
    and corresponding reference words.
    
    Args:
        response (str): The model's response.
        reference_text (str): The reference text (chunks).
        fuzzy_threshold (int): Similarity threshold for fuzzy matching (0-100).
    
    Returns:
        dict: Exact match percentage, fuzzy match percentage, combined match percentage,
              list of exactly matched words, and list of reference words.
    """
    # Exact matching
    exact_match_percentage, matched_words, reference_matches = exact_word_matching(response, reference_text)
    
    # Fuzzy matching
    fuzzy_match_percentage = fuzzy_word_matching(response, reference_text, fuzzy_threshold)
    
    # Combined matching (average of exact and fuzzy)
    combined_match_percentage = (exact_match_percentage + fuzzy_match_percentage) / 2
    
    return {
        "exact_match_percentage": exact_match_percentage,
        "fuzzy_match_percentage": fuzzy_match_percentage,
        "combined_match_percentage": combined_match_percentage,
        "matched_words": matched_words,  # List of exactly matched words
        "reference_words": reference_matches  # List of corresponding reference words
    }

def extract_unique_words(text):
    """
    Extract all unique words from a given text.
    
    Args:
        text (str): The input text.
    
    Returns:
        list: A list of unique words.
    """
    words = text.lower().split()
    unique_words = list(set(words))  # Remove duplicates
    return unique_words