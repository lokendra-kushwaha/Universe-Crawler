import sqlite3
import json
import pandas as pd

DB_NAME = "universe_search.db"

def init_db():
    """
    Creates the necessary SQL tables if they do not exist in the database file.
    """
    # Connect to SQLite (this automatically creates the file if missing)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Table for storing page text (for snippets)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DocumentStore (
            url TEXT PRIMARY KEY,
            page_text TEXT
        )
    ''')

    # 2. Table for storing Inverted Index
    # url_list will store a JSON string array of URLs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS InvertedIndex (
            word TEXT PRIMARY KEY,
            url_list TEXT 
        )
    ''')

    # 3. Table for storing Web Graph
    # target_urls will store a JSON string array of outgoing links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WebGraph (
            source_url TEXT PRIMARY KEY,
            target_urls TEXT
        )
    ''')

    # 4. Table for storing PageRank Scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PageRankScores (
            url TEXT PRIMARY KEY,
            score REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ System Database initialized successfully.")


import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

@st.cache_resource(show_spinner=False)
def init_ai_components():
    """
    Initializes the heavy AI model and ChromaDB client only ONCE globally.
    Reuses the same memory instance across the entire application.
    """
    print("Loading AI Model and Vector Database into Global Cache...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.PersistentClient(path="./universe_vector_db")
    collection = chroma_client.get_or_create_collection(name="web_universe")
    
    return model, chroma_client, collection

def save_crawled_data(web_graph, inverted_index, page_texts, ranks):
    """
    Saves the dynamically crawled data into the SQLite relational database 
    and the ChromaDB vector database for AI semantic search.
    
    Uses batch processing for generating embeddings to ensure maximum performance,
    and 'upsert' operations to update existing URLs seamlessly.

    Args:
        web_graph (dict): Mapping of source URLs to target URLs.
        inverted_index (dict): Mapping of words to sets of URLs.
        page_texts (dict): Mapping of URLs to their extracted text.
        ranks (dict): Calculated PageRank scores for each URL.

    Returns:
        None
    """
    # ==========================================
    # 1. SQLITE DATABASE PERSISTENCE
    # ==========================================
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Save Page Texts (Document Store)
    for url, text in page_texts.items():
        cursor.execute('''
            INSERT OR REPLACE INTO DocumentStore (url, page_text) 
            VALUES (?, ?)
        ''', (url, text))

    # Save Inverted Index (Converting Python Sets to JSON Arrays)
    for word, urls in inverted_index.items():
        url_list_json = json.dumps(list(urls))
        cursor.execute('''
            INSERT OR REPLACE INTO InvertedIndex (word, url_list) 
            VALUES (?, ?)
        ''', (word, url_list_json))

    # Save Web Graph (Converting Python Lists to JSON Arrays)
    for source_url, target_urls in web_graph.items():
        target_urls_json = json.dumps(target_urls)
        cursor.execute('''
            INSERT OR REPLACE INTO WebGraph (source_url, target_urls) 
            VALUES (?, ?)
        ''', (source_url, target_urls_json))

    # Save PageRank Scores
    for url, score in ranks.items():
        cursor.execute('''
            INSERT OR REPLACE INTO PageRankScores (url, score) 
            VALUES (?, ?)
        ''', (url, float(score)))

    conn.commit()
    conn.close()
    
    # ==========================================
    # 2. CHROMADB VECTOR DATABASE PERSISTENCE
    # ==========================================
    
    # Retrieve the globally cached model and database collection
    model, chroma_client, collection = init_ai_components()

    # Prepare batch data for high-speed AI processing
    urls_list = list(page_texts.keys())
    texts_list = list(page_texts.values())
    
    # Check if there is data to save to avoid empty list errors
    if urls_list:
        print(f"Generating AI Vector Embeddings for {len(texts_list)} pages...")
        
        # Convert all texts into a batch of number arrays (Vector Embeddings)
        embeddings_list = model.encode(texts_list).tolist() 
        
        # Prepare metadata for filtering capabilities later
        metadatas_list = [{"url": u} for u in urls_list]

        # Use 'upsert' instead of 'add' to overwrite existing URLs without crashing
        collection.upsert(
            ids=urls_list,
            embeddings=embeddings_list,
            documents=texts_list,
            metadatas=metadatas_list
        )

    print("✅ Web graph, index data, and AI vectors successfully saved!")


def initialize_logs_table():
    """
    Creates a dedicated table for storing search analytics if it doesn't exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SearchLogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            results_count INTEGER,
            search_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def log_search(query, results_count, search_time):
    """
    Silently logs a user's search query and performance metrics into the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO SearchLogs (query, results_count, search_time) 
        VALUES (?, ?, ?)
    ''', (query, results_count, search_time))
    conn.commit()
    conn.close()

    
def get_admin_metrics():
    """
    Calculates and retrieves total searches and average speed for the dashboard.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Total Searches Executed
    cursor.execute("SELECT COUNT(*) FROM SearchLogs")
    total_searches = cursor.fetchone()[0]
    
    # 2. Average Search Speed
    cursor.execute("SELECT AVG(search_time) FROM SearchLogs")
    avg_time = cursor.fetchone()[0]
    if avg_time is None:
        avg_time = 0.0
        
    conn.close()
    return total_searches, avg_time


def get_top_queries(limit=10):
    """
    Fetches the most frequently searched keywords from the database.
    Groups identical queries and counts their occurrences.
    """
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT query AS "Search Keyword", COUNT(query) AS "Total Searches"
        FROM SearchLogs 
        GROUP BY query 
        ORDER BY "Total Searches" DESC 
        LIMIT ?
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df


def get_zero_result_queries(limit=10):
    """
    Fetches failed queries that returned 0 results.
    Helps the admin identify missing content in the search index.
    """
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT query AS "Failed Keyword", COUNT(query) AS "Attempts"
        FROM SearchLogs 
        WHERE results_count = 0 
        GROUP BY query 
        ORDER BY "Attempts" DESC 
        LIMIT ?
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

@st.cache_data(show_spinner=False)
def load_database():
    """
    Loads the entire database into memory for instant frontend searching.
    Returns empty data structures if the database has not been populated yet.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    web_graph = {}
    inverted_index = {}
    page_texts = {}
    ranks = {}

    try:
        # Load Document Store
        cursor.execute('SELECT url, page_text FROM DocumentStore')
        for row in cursor.fetchall():
            page_texts[row[0]] = row[1]

        # Load Inverted Index (Converting JSON back to Python Sets)
        cursor.execute('SELECT word, url_list FROM InvertedIndex')
        for row in cursor.fetchall():
            inverted_index[row[0]] = set(json.loads(row[1]))

        # Load Web Graph
        cursor.execute('SELECT source_url, target_urls FROM WebGraph')
        for row in cursor.fetchall():
            web_graph[row[0]] = json.loads(row[1])

        # Load PageRank Scores
        cursor.execute('SELECT url, score FROM PageRankScores')
        for row in cursor.fetchall():
            ranks[row[0]] = row[1]

    except sqlite3.OperationalError:
        print("⚠️ Database tables not found. System will start with empty memory.")

    conn.close()
    
    # Calculate unique pages dynamically from the loaded web graph
    unique_pages = list(web_graph.keys())
    
    return web_graph, inverted_index, page_texts, ranks, unique_pages


if __name__ == "__main__":
    init_db()