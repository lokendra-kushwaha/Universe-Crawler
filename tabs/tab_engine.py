import streamlit as st

def render_about_engine():
    """
    Renders the 'About the Engine' tab with technical details and PageRank mathematics.
    """
    st.markdown(r"""
    ## 🚀 Inside the Universe Crawler
    
    Welcome to the **Universe Crawler**, a custom-built, highly scalable hybrid search engine. 
    
    **The Development Journey:** 
    This engine is the result of a rigorous **1-month intensive development cycle**. The primary goal was to build the core mathematical ranking algorithms and AI semantics completely from scratch, moving away from off-the-shelf basic search libraries. While the deep algorithmic engineering took a full month to perfect and test locally, the final polishing, UI integration, and GitHub/Live deployment were rapidly executed over just a few days to bring this project to the public web.

    ---

    ### 🌐 1. Data Ingestion: Where Does the Data Come From?
    Unlike standard datasets downloaded from Kaggle, this engine builds its own universe dynamically from the live web. The data pipeline operates in three precise steps:
    * **Live Multi-threaded Web Crawling:** The crawler starts from user-defined "Seed URLs" (e.g., Wikipedia). Using `concurrent.futures`, it launches multiple worker threads to send HTTP requests, fetching live HTML from the internet simultaneously.
    * **Text Extraction & Cleaning:** It parses the raw HTML using BeautifulSoup, stripping away tags, scripts, and unnecessary spaces to extract pure, readable text.
    * **Link Harvesting:** Simultaneously, it extracts all outgoing hyperlinks (excluding media files) to map connections between pages. These new links are dynamically added to the crawl queue, allowing the engine to traverse deeper into the web universe, exactly like the original Googlebot.
    * **Data Persistence:** As pages are processed, the raw text and graph data are saved into a local SQLite database, while the AI vectors are stored persistently in ChromaDB for instant retrieval.

    ---

    ### 🧠 2. The Hybrid Search Architecture
    To provide the most accurate results, this engine does not rely on a single search method. It runs a **Hybrid Pipeline** combining two different technologies:
    
    * **Exact Match Engine (Inverted Index):** Uses a pre-computed dictionary (Hash Map) to find exact string matches in $O(1)$ time complexity. Perfect for specific technical terms, names, or IDs.
    * **AI Semantic Engine (ChromaDB + Sentence Transformers):** Uses the `all-MiniLM-L6-v2` AI model to convert web pages and user queries into 384-dimensional mathematical vectors. It understands the *meaning* and *context* of a query (e.g., matching "automobile" with "car") using Cosine Similarity.

    ---

    ### 🧮 3. The Mathematics of Authority (PageRank)
    Finding a keyword is easy, but ranking the results requires mathematical authority. This engine implements a custom version of the original **PageRank Algorithm** (developed by Larry Page and Sergey Brin).
    
    The engine analyzes the web graph (how pages link to each other) and calculates the probability that a random surfer will land on a specific page. The core mathematical formula driving our ranking is:
    
    $$PR(u) = (1 - d) + d \sum_{v \in B(u)} \frac{PR(v)}{L(v)}$$
    
    * **$PR(u)$**: The PageRank score of the target page $u$.
    * **$d$**: The Damping Factor (set to **0.85**), representing the probability that a user will continue clicking links.
    * **$B(u)$**: The set of all pages $v$ that link to page $u$.
    * **$L(v)$**: The total number of outbound links from page $v$.
    
    The engine runs this equation iteratively using Matrix Multiplication until the scores converge, ensuring that pages linked by other high-quality pages receive an exponential boost in ranking.

    ---

    ### ⚡ 4. Microsecond Execution & Speed
    If you look at the search results, you will notice response times measured in fractions of a second. How is this achieved in Python?
    
    * **Pre-Computed Indexing:** During the crawling phase, texts are tokenized and mapped into an Inverted Index. When a user searches, the engine doesn't scan documents; it simply looks up the pre-mapped URL sets, reducing search time to near zero.
    * **Batch Vector Processing:** AI embeddings are processed in batches using highly optimized C++ backends via the `thefuzz` and `sentence-transformers` libraries.
    * **Timer Precision:** The engine uses Python's `time.time()` module to capture the exact timestamp before and after the algorithmic execution, providing an authentic, microsecond-accurate latency report on the UI.

    ---

    ### 🛠️ 5. Next-Gen Quality of Life Features
    * **Fuzzy Auto-Correct:** Integrated with the Levenshtein Distance algorithm, the engine detects typos and spelling mistakes in real-time, offering a Google-style *"Did you mean...?"* suggestion to prevent dead-end searches.
    * **Multithreaded Crawling:** The backend utilizes concurrent processing, allowing the crawler to map the web universe efficiently without freezing the main thread.
    * **Responsive Native UI:** Built with Streamlit but heavily customized with fluid CSS, media queries, and dynamic session states to deliver a seamless, app-like experience across both desktop and mobile devices.
    
    <br>
    <p style="text-align: center; color: #666; font-size: 0.9rem;">
    <i>Engineered from scratch by Lokendra Kushwaha © 2026</i>
    </p>
    """, unsafe_allow_html=True)