import re
import chromadb
from sentence_transformers import SentenceTransformer
from thefuzz import process

# ==========================================
# GLOBAL INITIALIZATION
# ==========================================
# Load the AI model and Vector DB outside the function so they don't reload on every search
print("Loading AI Semantic Search Engine...")
try:
    ai_search_model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.PersistentClient(path="./universe_vector_db")

    # Use get_or_create_collection so it never crashes even if the DB is empty
    vector_collection = chroma_client.get_or_create_collection(name="web_universe")
except Exception as e:
    print(f"Vector DB not initialized yet. Run the crawler first! Error: {e}")
    vector_collection = None


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
    # Safety checks to prevent crashes if DB failed to load or is completely empty
    if vector_collection is None:
        print("Vector collection is not initialized.")
        return []
        
    if vector_collection.count() == 0:
        print("Vector database is empty. Please run the crawler first.")
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
        
    highlighted_snippet = re.sub(
        f"({query})", 
        r"<b style='color: #202124;'>\1</b>", 
        clean_snippet, 
        flags=re.IGNORECASE
    )
    
    return f"...{highlighted_snippet}..."


def get_did_you_mean(query, index_keys, threshold=70):
    """
    Uses Levenshtein distance to find the closest matching word in the index.
    
    Args:
        query (str): The misspelled word.
        index_keys (list): The list of all words available in the inverted index.
        threshold (int): Minimum match score (0-100) to consider it a valid suggestion.
        
    Returns:
        str: The closest matching word if found, otherwise None.
    """
    if not index_keys:
        return None
        
    # Extract the absolute best match and its score (out of 100)
    best_match, score = process.extractOne(query.lower(), index_keys)
    
    # If the score is high enough but not an exact 100 match, return the suggestion
    if score >= threshold and score < 100:
        return best_match
        
    return None