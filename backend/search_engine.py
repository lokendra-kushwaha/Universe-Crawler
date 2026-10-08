import re
import streamlit as st
from thefuzz import process
from backend.db_manager import init_ai_components


def ai_semantic_search(query, ranks_dict, max_results=10):
    """
    Performs an AI-powered semantic search by converting the user's query into a vector 
    and finding the closest matching pages in the ChromaDB vector database.
    
    Merges the AI semantic similarity score with the PageRank authority score 
    to produce a highly accurate final ranking.

    Args:
        query (str): The natural language query from the user.
        ranks_dict (dict): A dictionary mapping URLs to their PageRank scores (e.g., {url: score}).
        max_results (int): The maximum number of results to retrieve from the vector database.

    Returns:
        list: A list of tuples formatted as (URL, Final_Score), sorted in descending order of relevance and authority.
              Returns an empty list if no matches are found.
    """
    try:
        # 1. Get the cached model and db (loads instantly from cache)
        ai_search_model, chroma_client, vector_collection = init_ai_components()
        
        # 2. Check if the collection is empty before searching
        if vector_collection is None or vector_collection.count() == 0:
            print("⚠️ Vector database is empty. Please run the crawler first!")
            return []
            
    except Exception as e:
        print(f"⚠️ Vector DB Error: {e}")
        return []

    # 1. Convert the user query into a mathematical vector
    query_vector = ai_search_model.encode(query).tolist()
    
    # 2. Query ChromaDB for the closest vector matches
    # ChromaDB returns 'distances' (lower distance = closer meaning)
    ai_results = vector_collection.query(
        query_embeddings=[query_vector],
        n_results=max_results
    )
    
    # Check if we got any results back
    if not ai_results['ids'] or not ai_results['ids'][0]:
        return []
        
    matched_urls = ai_results['ids'][0]
    distances = ai_results['distances'][0]
    
    search_results = []
    
    # 3. Score Fusion: Merge AI Semantic Score with PageRank Authority
    for i in range(len(matched_urls)):
        url = matched_urls[i]
        distance = distances[i]
        
        # Convert ChromaDB distance to a similarity score (higher is better)
        # We add 1.0 to avoid division by zero
        semantic_score = 1.0 / (1.0 + distance) 
        
        # Get the PageRank score from the dictionary (default to 0.0 if missing)
        pagerank_score = ranks_dict.get(url, 0.0)
        
        # The Master Equation: 70% Relevance (AI) + 30% Authority (PageRank)
        final_score = (semantic_score * 0.7) + (pagerank_score * 0.3)
        
        # Bundle the URL and its new fused score
        search_results.append((url, final_score))
        
    # 4. Sort the tuples by the highest final score
    search_results.sort(key=lambda x: x[1], reverse=True)
    
    return search_results


@st.cache_data(show_spinner=False, ttl=3600)
def search(query, inverted_index, unique_pages, ranks):
    """
    Searches the inverted index for a keyword and ranks the resulting URLs by their PageRank score.

    This function bridges Phase 1 (Data Extraction) and Phase 2 (Mathematical Authority). 
    It retrieves the raw set of URLs containing the keyword, maps each URL to its pre-calculated 
    PageRank score using the master index, and returns a sorted ranking.

    Args:
        query (str): The keyword to search for (e.g., "poetry", "einstein").
        inverted_index (dict): The dictionary mapping words to a set of URLs where they appear.
        unique_pages (list): The master list acting as the index (roll number) for all URLs.
        ranks (numpy.ndarray): The 1D array containing the final PageRank score for each URL.

    Returns:
        list: A list of tuples formatted as (URL, Score), sorted in descending order of Authority. 
              Returns an empty list if the query word is not found in the index.
    """
    query = query.lower()
    
    # 1. Look up the query in our dictionary
    if query not in inverted_index:
        return []
        
    matched_urls = inverted_index[query]
    search_results = []
    
    # 2. Attach the PageRank score to each matched URL (Authority Mapping)
    for url in matched_urls:
        # Ensure the URL exists in our master list to avoid index errors
        if url in unique_pages:
            url_index = unique_pages.index(url)
            score = ranks[url_index]
            
            # Bundle the URL and its score into a tuple and add it to our results list
            search_results.append((url, score))
            
    # 3. Sort the tuples to determine the final ranking
    # lambda x: x[1] tells the sort function to evaluate the 'score' (index 1) rather than the 'url' (index 0)
    search_results.sort(key=lambda x: x[1], reverse=True)
    
    return search_results


def get_best_snippet(full_text, query, padding=60):
    """
    Finds the keyword in the text, extracts a clean snippet, and highlights the keyword.
    Acts as an independent text-processing tool for the search engine.
    """
    lower_text = full_text.lower()
    query = query.lower()
    
    match_index = lower_text.find(query)
    
    if match_index == -1:
        return full_text[:100].strip() + "..."
        
    start_pos = max(0, match_index - padding)
    end_pos = min(len(full_text), match_index + len(query) + padding)
    
    raw_snippet = full_text[start_pos:end_pos]
    
    words = raw_snippet.split(" ")
    if len(words) > 2:
        clean_snippet = " ".join(words[1:-1])
    else:
        clean_snippet = raw_snippet
        
    safe_query = re.escape(query)

    highlighted_snippet = re.sub(
        f"({safe_query})", 
        r"<b>\1</b>", 
        clean_snippet, 
        flags=re.IGNORECASE
    )
    
    return f"...{highlighted_snippet}..."


# def get_did_you_mean(query, index_keys, threshold=70):
#     """
#     Uses Levenshtein distance to find the closest matching word in the index.
    
#     Args:
#         query (str): The misspelled word.
#         index_keys (list): The list of all words available in the inverted index.
#         threshold (int): Minimum match score (0-100) to consider it a valid suggestion.
        
#     Returns:
#         str: The closest matching word if found, otherwise None.
#     """
#     if not index_keys:
#         return None
        
#     # Extract the absolute best match and its score (out of 100)
#     best_match, score = process.extractOne(query.lower(), index_keys)
    
#     # If the score is high enough but not an exact 100 match, return the suggestion
#     if score >= threshold and score < 100:
#         return best_match
        
#     return None


def get_did_you_mean(query, index_keys, threshold=70):
    """
    Optimized fuzzy search utilizing Search Space Reduction to achieve millisecond execution.
    Filters the massive database index by initial character and string length bounds 
    before applying the Levenshtein distance algorithm.

    Args:
        query (str): The misspelled keyword entered by the user.
        index_keys (list): The complete list of all unique words in the inverted index.
        threshold (int): Minimum match score (0-100) required to consider it a valid suggestion.

    Returns:
        str: The closest matching word if the score meets the threshold, otherwise None.
    """
    if not query or not index_keys:
        return None
        
    query = query.lower()
    first_char = query[0]
    
    # Keep only words starting with the same letter
    optimized_search_space = [
        word for word in index_keys 
        if word and word.startswith(first_char)
    ]
    
    # 2. If the user misspelled the very first letter (e.g., 'xata' instead of 'data'),
    # the optimized space will be empty. Fall back to the full index to ensure a result.
    search_space = optimized_search_space if optimized_search_space else index_keys

    # 3. Execute Levenshtein distance on the drastically reduced list
    result = process.extractOne(query, search_space)
    
    # process.extractOne returns a tuple (best_match, score) or None if the list was invalid
    if result:
        best_match, score = result
        if score >= threshold and score < 100:
            return best_match
            
    return None