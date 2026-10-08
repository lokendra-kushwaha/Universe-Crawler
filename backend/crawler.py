import requests
import re
import concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag

def extract_clean_text(soup):
    """
    Extracts and cleans raw text from a BeautifulSoup object.

    This function removes excess whitespace, tabs, and newlines from the parsed 
    HTML to generate a clean, continuous string suitable for search snippets.

    Args:
        soup (BeautifulSoup): The parsed HTML object of the web page.

    Returns:
        str: A clean, single-line string containing the visible text of the page.
    """
    # Extract raw text, replacing HTML tags with spaces to prevent word merging
    raw_text = soup.get_text(separator=' ')
    
    # Use regular expressions to replace multiple spaces or newlines with a single space
    clean_text = re.sub(r'\s+', ' ', raw_text).strip()
    return clean_text


def fetch_and_parse_url(url):
    """Fetches a URL and extracts its text and outgoing links.

    This function is designed to be executed by individual worker threads. 
    It handles network requests, parses the HTML, cleans the text, and filters 
    out invalid or non-text outgoing links.

    Args:
        url (str): The target URL to crawl and parse.

    Returns:
        tuple: A tuple containing:
            - url (str): The crawled URL.
            - clean_page_text (str or None): The extracted text, or None if failed.
            - out_links (list or None): A list of valid outgoing HTTP/HTTPS links.
            - error (str or None): An error message if the request failed, otherwise None.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # Abort if the page does not return a successful HTTP status
        if response.status_code != 200:
            return url, None, None, f"Status: {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        clean_page_text = extract_clean_text(soup)
        
        out_links = []
        
        # Extract and normalize all anchor tags with href attributes
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_link = urljoin(url, href)
            
            # Remove URL fragments (e.g., #section) to avoid duplicate indexing
            full_link, _ = urldefrag(full_link)
            
            # Filter out direct media files and non-HTTP protocols
            bad_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.mp4', '.zip', '.exe', '.svg']
            is_media = any(full_link.lower().endswith(ext) for ext in bad_extensions)
            
            if full_link.startswith('http') and not is_media:
                out_links.append(full_link)
                
        return url, clean_page_text, out_links, None
        
    except Exception as e:
        return url, None, None, str(e)


def build_web_graph(seed_urls, max_pages=10, max_workers=10, ui_callback=None):
    """Crawls a list of seed URLs concurrently to build a web graph and inverted index.

    Utilizes a ThreadPoolExecutor to crawl multiple pages simultaneously. 
    It manages state without complex locks by aggregating thread results centrally.

    Args:
        seed_urls (list): A list of starting URLs (e.g., ["https://site1.com"]).
        max_pages (int, optional): The maximum number of pages to crawl. Defaults to 10.
        ui_callback (callable, optional): A function to update the frontend UI progress. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - web_graph (dict): A dictionary mapping URLs to lists of outgoing links.
            - inverted_index (dict): A dictionary mapping words to sets of URLs.
            - page_texts (dict): A dictionary mapping URLs to their clean text snippets.
    """
    to_visit = seed_urls.copy()  
    visited = set()
    queued = set(seed_urls) 
           
    web_graph = {}
    inverted_index = {}
    page_texts = {} 
    pages_crawled = 0
    
    # Initialize a ThreadPoolExecutor with up to 10 concurrent workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        
        while to_visit and pages_crawled < max_pages:
            
            # Determine the batch size to avoid exceeding the max_pages limit
            batch_size = min(10, max_pages - pages_crawled, len(to_visit))
            
            current_batch = []
            for _ in range(batch_size):
                url = to_visit.pop(0)
                current_batch.append(url)
                visited.add(url)
                
            # Dispatch network tasks to the worker threads
            futures = {executor.submit(fetch_and_parse_url, url): url for url in current_batch}
            
            # Process results sequentially as threads complete their tasks
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                url, clean_text, out_links, error = future.result()
                
                pages_crawled += 1
                
                if ui_callback:
                    ui_callback(f"[{pages_crawled}/{max_pages}] {url}")
                print(f"🚀 [Turbo Crawl {pages_crawled}/{max_pages}]: {url}")
                
                if error or not clean_text:
                    print(f"⚠️ Error on {url}: {error}")
                    web_graph[url] = []
                    continue
                
                # 1. Store the clean text for UI context snippets
                page_texts[url] = clean_text
                web_graph[url] = []
                
                # 2. Tokenize the text and populate the inverted index
                words = clean_text.lower().split()
                for word in words:
                    if word not in inverted_index:
                        inverted_index[word] = set()
                    inverted_index[word].add(url)
                    
                # 3. Update the web graph and append new discoveries to the queue
                for link in out_links:
                    if link not in queued and link not in visited:
                        to_visit.append(link)
                        queued.add(link) 
                    web_graph[url].append(link)

    return web_graph, inverted_index, page_texts
