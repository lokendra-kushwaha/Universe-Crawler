import streamlit as st
import streamlit.components.v1 as components
import time
import plotly.express as px
from urllib.parse import urlparse
from crawler import build_web_graph
from page_rank import calculate_pagerank 
from search_engine import ai_semantic_search, search, get_did_you_mean, get_best_snippet
from db_manager import init_db, save_crawled_data, initialize_logs_table, log_search, get_admin_metrics, load_database, get_top_queries, get_zero_result_queries
import pandas as pd
import math

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(page_title="Universe Crawler", page_icon="🌌", layout="wide")

# --- CUSTOM CSS FOR RESPONSIVE DESIGN ---
st.markdown("""
    <style>
    /* Main Titles */
    .main-title {
        text-align: center; 
        font-size: clamp(2rem, 6vw, 3.5rem); 
        font-weight: 800; 
        margin-bottom: 5px; 
        margin-top: -20px;
        line-height: 1.2;
    }
    .sub-title {
        text-align: center; 
        color: #555555; /* Darkened for Light Mode */
        font-size: clamp(0.9rem, 2.5vw, 1.2rem); 
        margin-bottom: 40px;
    }
    
    /* Search Results UI (LIGHT MODE COLORS) */
    .result-header {
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        font-weight: 600;
        margin-bottom: 15px;
        color: #333333; /* Dark Grey for clear visibility */
    }
    .result-card {
        padding: 5px 0 15px 0;
    }
    .result-title {
        font-size: clamp(1.1rem, 2.5vw, 1.3rem);
        font-weight: 500;
        margin-bottom: 3px;
        line-height: 1.3;
    }
    .result-title a {
        text-decoration: none;
        color: #1a0dab; /* Classic Search Blue */
    }
    .result-title a:hover {
        text-decoration: underline;
    }
    .result-url {
        font-size: clamp(0.75rem, 2vw, 0.85rem);
        color: #006621; /* Classic Dark Green */
        word-break: break-all; 
        margin-bottom: 5px;
    }
    
    @media (max-width: 768px) {
        .main-title { margin-top: 10px; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Session State Initialization (Memory)
# ==========================================
if 'is_crawled' not in st.session_state:
    # Initialize database tables if they do not exist
    init_db() 
    initialize_logs_table()

    # Load existing data from the SQLite database
    web_graph, inverted_index, page_texts, ranks, unique_pages = load_database()
    
    # Populate Streamlit's session state with the loaded database records
    st.session_state['web_graph'] = web_graph
    st.session_state['inverted_index'] = inverted_index
    st.session_state['page_texts'] = page_texts
    st.session_state['unique_pages'] = unique_pages
    
    # Ensure PageRank scores are stored as a structured list corresponding to unique_pages
    if isinstance(ranks, dict) and unique_pages:
        st.session_state['ranks'] = [ranks.get(page, 0.0) for page in unique_pages]
    else:
        st.session_state['ranks'] = ranks
        
    # Automatically activate the search UI and dashboard if data already exists
    if web_graph:
        st.session_state['is_crawled'] = True
    else:
        st.session_state['is_crawled'] = False


# ==========================================
# CRAWLER CONTROL PANEL (Hidden in Expander)
# ==========================================

with st.expander("🚀 Help Grow the Universe (Index New Websites)", expanded=False):
    
    st.markdown("""
        <style>
        .custom-crawler-title {
            font-size: 1.5rem;
            font-weight: 800;
            text-align: center;
            color: #222222;
            line-height: 1.2;
        }
        .custom-crawler-quote {
            font-size: 0.9rem;
            color: #666666;
            text-align: center;
            font-style: italic;
            margin-top: 5px;
            margin-bottom: 25px;
        }
        
        /* 📱 Media Query: */
        @media (max-width: 320px) {
            .custom-crawler-title { font-size: 1.2rem; }
            .custom-crawler-quote { font-size: 0.8rem; }
        }

        @media screen and (max-width: 768px) {
        /* Targets the expander title text on mobile */
        div[data-testid="stExpander"] summary p {
            font-size: 0.82rem !important; /* Adjust size if needed */
            white-space: nowrap !important; 
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            }
        }

        /* ========================================= */
        /* EXPANDER (Crawler Box)    */
        /* ========================================= */
        
        /* 1. Main Box: Glowing Blue Border & Soft Shadow */
        div[data-testid="stExpander"] {
            border: 1.5px solid #1a73e8 !important; /* Google Blue */
            border-radius: 10px !important;
            box-shadow: 0 4px 20px rgba(26, 115, 232, 0.12) !important;
            background: linear-gradient(145deg, #ffffff, #f8faff) !important;
            transition: all 0.3s ease-in-out !important;
        }

        /* 2. Hover Effect: Glow gets slightly stronger */
        div[data-testid="stExpander"]:hover {
            box-shadow: 0 6px 25px rgba(26, 115, 232, 0.22) !important;
        }

        /* 3. Expander Header (The clickable bar) */
        div[data-testid="stExpander"] summary {
            background-color: #e8f0fe !important; /* Very light blue background */
            padding: 5px 10px !important;
            border-radius: 8px 8px 0 0 !important;
        }

        /* 4. Text inside the Expander Header */
        div[data-testid="stExpander"] summary p {
            color: #1557b0 !important; /* Deep Premium Blue */
            font-weight: 700 !important;
            letter-spacing: 0.3px !important;
        }
        
        /* 5. The line icon (chevron) color */
        div[data-testid="stExpander"] summary svg {
            fill: #1a73e8 !important;
            color: #1a73e8 !important;
        }
        </style>
        
        <div class="custom-crawler-title">🕷️ Crawl The Universe</div>
        <div class="custom-crawler-quote">"Define your search universe"</div>
    """, unsafe_allow_html=True)

    # Grid Layout for Input & Controls
    c_col1, c_col2 = st.columns([2, 1], gap="medium")

    with c_col1:
        st.markdown(
            """
            <div style="font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                🌱 Enter Seed URLs or 
                <a href="#" target="_blank" style="color: #1f77b4; text-decoration: none; border-bottom: 1.5px dashed #1f77b4; padding-bottom: 1px; transition: 0.3s;">
                    Choose from here
                </a>
                <br>
                <span style="font-size: 12px; font-weight: normal; color: #7f8c8d; margin-left: 5px;">
                    (one URL per line)
                </span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        seed_urls_input = st.text_area(
            label="hidden_seed_label", 
            value="https://en.wikipedia.org/wiki/Data_science\nhttps://en.wikipedia.org/wiki/Artificial_intelligence",
            height=150,
            label_visibility="collapsed"
        )
        
    with c_col2:
        st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 8px;'>⚙️ Crawl Settings</div>", unsafe_allow_html=True)
        use_custom_limit = st.checkbox("🔓 Unlock Custom Limit")
        
        if use_custom_limit:
            # Pro Mode
            max_pages = st.number_input(
                "Enter Exact Max Pages:", 
                min_value=1, 
                max_value=9_007_199_254_740_991, 
                value=500, 
                step=50
            )
        else:
            # Normal Mode
            max_pages = st.slider(
                "Max Pages to Crawl:", 
                min_value=10, 
                max_value=500, 
                value=50, 
                step=10
            )
            
    # Centered Button and Terminal
    st.markdown("<br>", unsafe_allow_html=True)
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])

    with b_col2:
        start_button = st.button("🚀 Start Web Crawler", type="primary", use_container_width=True)
        
    # The Crawling Logic
    if start_button:
        raw_urls = seed_urls_input.split('\n')
        seed_urls = [url.strip() for url in raw_urls if url.strip().startswith("http")]
        
        if not seed_urls:
            st.error("Please enter at least one valid URL starting with http:// or https://")
        else:
            # TERMINAL SETUP
            terminal_box = st.empty() 
            log_data = ["> INITIALIZING MULTI-SEED CRAWLER...\n"] 
            terminal_box.code(log_data[0], language='bash')
            
            def update_ui(msg):
                log_data[0] += "> CRAWLING: " + msg + "\n"
                lines = log_data[0].split('\n')
                if len(lines) > 8: 
                    log_data[0] = '\n'.join(lines[-8:])
                terminal_box.code(log_data[0], language='bash')

            start_crawl_time = time.time()
            web_graph, inverted_index, page_texts = build_web_graph(seed_urls, max_pages=max_pages, ui_callback=update_ui)
            
            if web_graph:
                unique_pages, ranks = calculate_pagerank(web_graph)
                end_crawl_time = time.time()
                total_crawl_time = end_crawl_time - start_crawl_time 

                ranks_dict = {page: float(score) for page, score in zip(unique_pages, ranks)}
                save_crawled_data(web_graph, inverted_index, page_texts, ranks_dict)
                
                st.session_state['inverted_index'] = inverted_index
                st.session_state['unique_pages'] = unique_pages
                st.session_state['ranks'] = ranks
                st.session_state['page_texts'] = page_texts
                st.session_state['web_graph'] = web_graph
                st.session_state['is_crawled'] = True
                
                log_data[0] += f"\n> ✅ MATRIX GENERATED.\n> ✅ PAGERANK CALCULATED in {total_crawl_time:.2f}s."
                terminal_box.code(log_data[0], language='bash')
                st.success(f"✅ Indexed {len(unique_pages)} pages in {total_crawl_time:.2f} seconds!")
            else:
                st.error("⚠️ Failed to crawl. The target websites might be blocking bots.")


# ==========================================
# 5. UI: MAIN AREA (The Search Engine)
# ==========================================
st.markdown("""
    <style>
    /* ========================================= */
    /* 1. GLOBAL & STREAMLIT OVERRIDES           */
    /* ========================================= */
    
    /* Make Streamlit's default top menu transparent */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Push the main app content down to prevent overlap with fixed header */
    .block-container {
        padding-top: 180px !important; 
    }

    /* ========================================= */
    /* 2. CUSTOM DESKTOP COMPONENTS              */
    /* ========================================= */
    
    /* The Sticky Header Box */
    .fixed-main-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(12px); 
        -webkit-backdrop-filter: blur(12px);
        z-index: 999;
        text-align: center;
        padding-top: 65px; 
        padding-bottom: 20px;
        border-bottom: 1px solid #eaeaea;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.03);
    }
    
    /* Fluid Typography for the Sticky Text */
    .sticky-title {
        font-size: clamp(1.8rem, 5vw, 3.5rem); 
        font-weight: 800; 
        line-height: 1.2;
        color: #222222;
        margin-bottom: 5px;
    }
    
    .sticky-subtitle {
        color: #666666; 
        font-size: clamp(0.85rem, 2vw, 1.2rem); 
        padding: 0 10px; 
    }

    /* Responsive Search Title */
    .responsive-search-title {
        color: #444444; 
        font-weight: 600; 
        margin-top: -10px;
        margin-bottom: 10px;
        font-size: 1.4rem; 
    }

    /* ========================================= */
    /* 1. FLOATING SEARCH BAR                    */
    /* ========================================= */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        border-radius: 30px !important;
        border: 1px solid #dfe1e5 !important;
        background-color: #ffffff !important;
        box-shadow: 0px 4px 10px rgba(32, 33, 36, 0.08) !important;
        transition: box-shadow 0.3s ease-in-out !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        box-shadow: 0px 6px 14px rgba(32, 33, 36, 0.15) !important;
        border: 1px solid #1a73e8 !important; 
    }
    div[data-testid="stTextInput"] input {
        padding: 12px 18px !important; 
        font-size: 0.83rem !important; 
    }
    
    /* ========================================= */
    /* 3. TABLET OPTIMIZATIONS (Max Width: 768px)*/
    /* ========================================= */
    @media screen and (max-width: 768px) {
        .fixed-main-header {
            padding-top: 65px; 
        }
        /* Slightly reduce gap for tablet screens */
        .block-container {
            padding-top: 150px !important; 
        }
    }

    /* ========================================= */
    /* 4. COMPACT MOBILE VIEW (Max Width: 600px) */
    /* ========================================= */
    @media screen and (max-width: 600px) {
        
        /* Perfectly balanced padding to clear the header without massive gaps */
        .block-container {
            padding-top: 170px !important; 
        }
        
        /* Pull the Custom HTML Header slightly down */
        .fixed-main-header {
            margin-bottom: -15px !important;
        }
        
        /* Adjust Search Title for smaller screens */
        .responsive-search-title {
            font-size: 1.1rem !important; 
            margin-top: 5px !important; 
            margin-bottom: 0px !important; 
            margin-left: -10px !important;
        }

        
        /* ========================================= */
        /* ANALYTICS DASHBOARD TITLE STYLING         */
        /* ========================================= */

        .analytics-dashboard-title {
            font-size: 1.4rem !important;        /* Perfect size for mobile screens */
            font-weight: 800 !important;         /* Makes the text bold and strong */
            text-align: center !important;       /* Centers the title to match the tabs */
            color: #1a73e8 !important;           /* Professional Google Blue color */
            margin-top: 15px !important;         /* Space above (from tabs) */
            margin-bottom: 25px !important;      /* Space below (from metrics) */
            line-height: 1.3 !important;         /* Keeps spacing clean if text wraps to 2 lines */
            padding-bottom: 12px !important;     
            border-bottom: 2px solid #e8eaed !important; /* Sleek underline separator */
            letter-spacing: 0.3px !important;    /* Slight letter spacing for a premium feel */
        }

        /* ========================================= */
        /* MARKDOWN HEADINGS RESIZING FOR MOBILE     */
        /* ========================================= */
        
        /* ## (Heading 2) ko target karne ke liye */
        div[data-testid="stMarkdownContainer"] h2 {
            font-size: 1.4rem !important;
            line-height: 1.2 !important;
            margin-top: 10px !important;
        }

        div[data-testid="stMarkdownContainer"] h3 {
            font-size: 1.1rem !important;
            line-height: 1.2 !important;
        }
        
        /* Pull the Database Status box (st.info/st.success) up */
        div[data-testid="stAlert"] {
            margin-top: -15px !important;
        }
        
        /* Tightly pack Sliders & Stacked Columns */
        div[data-testid="stSlider"] {
            margin-bottom: -20px !important;
            padding-bottom: 0px !important;
        }
        div[data-testid="column"] {
            margin-bottom: -25px !important;
        }

    }

    /* ========================================= */
    /* BULLETPROOF GRID LAYOUT FOR TABS          */
    /* ========================================= */
        
        div[role="tablist"] {
            display: flex !important;
            flex-wrap: wrap !important;
            justify-content: center !important; /* Centers the items */
            align-items: center !important;
            gap: 1px 10px !important;
            width: 100% !important;
            margin-left: auto !important;  /* Pushes container to absolute center */
            margin-right: auto !important; /* Pushes container to absolute center */
            margin-top: -25px !important;
            padding-bottom: 5px !important;
        }

        button[role="tab"] {
            flex: 0 0 42% !important;
            margin: 0px !important;
            background-color: #f9f9f9 !important;
            border-radius: 8px !important;
            border: 1px solid #e5e5e5 !important;
            padding: 8px 5px !important;
        }
        
        /* 3. Keep text centered and wrapped */
        button[role="tab"] p, button[role="tab"] div {
            font-size: 0.72rem !important; 
            font-weight: 600 !important;
            white-space: normal !important; 
            text-align: center !important;
            margin: 0 !important;
            line-height: 1.3 !important;
        }

    /* ========================================= */
    /* PREMIUM UI UPGRADES (STATUS & BUTTON)     */
    /* ========================================= */

        /* 1. Dashboard Style Database Status Card */
        div[data-testid="stAlert"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-left: 4px solid #1a73e8 !important; /* Blue accent */
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
            padding: 15px 20px !important;
            color: #202124 !important;
            font-weight: 500 !important;
        }

        /* 2. High-Tech Sidebar Crawler Button */
        section[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #1a73e8, #0d47a1) !important;
            border: none !important;
            border-radius: 8px !important;
            color: white !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 10px rgba(26, 115, 232, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Sidebar Button Hover Animation */
        section[data-testid="stSidebar"] button[kind="primary"]:hover {
            box-shadow: 0 6px 14px rgba(26, 115, 232, 0.4) !important;
            transform: translateY(-2px) !important;
            background: linear-gradient(135deg, #1557b0, #0a3880) !important;
        }

    /* ========================================= */
    /* STYLE SEGMENTED CONTROLS (RADIO PILLS)*/
    /* ========================================= */

        /* 1. Main container background (Light Gray Pill) */
        div[role="radiogroup"] {
            background-color: #f1f3f4 !important;
            padding: 4px !important;
            border-radius: 30px !important;
            display: inline-flex !important;
            gap: 0 !important;
            border: 1px solid #e8eaed !important;
            width: fit-content !important;
        }

        /* 2. Hide the default radio circles permanently */
        div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        /* 3. Default styling for unselected options */
        div[role="radiogroup"] label {
            padding: 8px 24px !important;
            margin: 0 !important;
            border-radius: 25px !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            background-color: transparent !important;
            color: #5f6368 !important;
        }

        /* 4. Fix text margins inside the label */
        div[role="radiogroup"] label div {
            margin: 0 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }

        /* 5. The Magic: Styling the ACTIVE (Selected) option */
        div[role="radiogroup"] label:has(input:checked) {
            background-color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;
            color: #1a73e8 !important; /* Premium Google Blue text */
        }
        
        /* 6. Active state text styling */
        div[role="radiogroup"] label:has(input:checked) div {
            font-weight: 700 !important;
        }

    /* ========================================= */
    /* MOBILE FIX FOR RADIO PILLS (50/50 WIDTH)  */
    /* ========================================= */
    
    @media screen and (max-width: 768px) {
        div[role="radiogroup"] {
            display: flex !important;
            width: 100% !important;
        }

        /* 2. Dono buttons ko exactly 50% width do */
        div[role="radiogroup"] label {
            flex: 1 !important;
            width: 50% !important;
            padding: 8px 4px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        div[role="radiogroup"] label div {
            font-size: 0.75rem !important;
            text-align: center !important;
            line-height: 1.2 !important;
            white-space: normal !important;
        }
    }
    </style>
    
    <!-- ======================================= -->
    <!-- THE HTML STRUCTURE                      -->
    <!-- ======================================= -->
    <div class="fixed-main-header">
        <div class="sticky-title">🌌 Universe Crawler</div>
        <div class="sticky-subtitle">Navigate, map, and index the web universe in real-time.</div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.get('is_crawled', False):
    # Display statistics of the current database
    st.info(f"📊 **Database Status:** {len(st.session_state['unique_pages'])} total URLs indexed and ranked.")
    
    # Phase 3: The Search Input
    st.markdown("<br>", unsafe_allow_html=True)

    # Create two premium tabs
    tab_search, tab_crawl, tab_insights, tab_about, tab_me, tab_admin = st.tabs([
    "🔍 Search Engine",
    "🕷️ Expand & Crawl", 
    "📊 Universe Insights", 
    "💡 About Engine", 
    "👨‍💻 About Me",
    "⚙️ Admin Dashboard"
])
    
    # ==========================================
    # TAB 1: THE SEARCH ENGINE
    # ==========================================
    with tab_search:
        st.markdown('<h4 class="responsive-search-title">🔍 Search Your Indexed Universe</h4>', unsafe_allow_html=True)
        
        # ------------------------------------------
        # NEW: PREMIUM SEARCH MODE TOGGLE
        # ------------------------------------------
        search_mode = st.radio(
            "Select Search Engine Mode:",
            ["🎯 Exact Keyword (Speed & Precision)", "🤖 AI Semantic (Meaning & Context)"],
            horizontal=True,
            help="Exact Keyword uses Inverted Index. AI Semantic uses Vector Embeddings to understand the meaning of your query."
        )

        # Initialize session memory
        if "my_search_key" not in st.session_state:
            st.session_state.my_search_key = ""

        # Sync function
        def sync_to_url():
            st.query_params["q"] = st.session_state.my_search_key

        # Check URL params
        if "q" in st.query_params and st.session_state.get("my_search_key") != st.query_params["q"]:
            st.session_state.my_search_key = st.query_params["q"]
        
        query = st.text_input(
            label="Search Your Indexed Universe",
            placeholder="Type your query (e.g., 'data science' or 'fastest cars') and press Enter...",
            label_visibility="collapsed",
            key="my_search_key",
            on_change=sync_to_url
        )

        # ==========================================
        # CUSTOM HTML DIV GRID FOR TRENDING SEARCHES
        # ==========================================
        trending_html = """
        <style>
            /* Default Layout for PC: 6 buttons in one row */
            .custom-trending-div {
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 10px;
                margin-top: 5px;
                margin-bottom: 25px;
            }
            
            /* Mobile Layout: Exactly 3 buttons per row automatically */
            @media screen and (max-width: 650px) {
                .custom-trending-div {
                    grid-template-columns: repeat(3, 1fr);
                    gap: 8px;
                }
            }

            /* Premium Chip Button Styling */
            .custom-chip {
                display: block;
                background-color: #ffffff;
                border: 1px solid #dfe1e5;
                padding: 8px 5px;
                border-radius: 20px;
                text-align: center;
                text-decoration: none !important; /* Removes underline from links */
                color: #3c4043;
                font-size: 0.8rem;
                font-family: sans-serif;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                transition: all 0.2s ease-in-out;
            }
            
            /* Hover effect */
            .custom-chip:hover {
                background-color: #f8f9fa;
                border-color: #dadce0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                color: #202124;
            }
        </style>

        <p style='font-size: 0.85rem; color: #5f6368; margin-bottom: 8px;'>💡 Trending Searches:</p>
        <div class="custom-trending-div">
            <a href="?q=AI+News" target="_self" class="custom-chip">🤖 AI</a>
            <a href="?q=Fast+Cars" target="_self" class="custom-chip">🏎️ Cars</a>
            <a href="?q=Data+Science" target="_self" class="custom-chip">📊 Data</a>
            <a href="?q=Python" target="_self" class="custom-chip">🐍 Python</a>
            <a href="?q=Space" target="_self" class="custom-chip">🚀 Space</a>
            <a href="?q=Technology" target="_self" class="custom-chip">💻 Tech</a>
        </div>
        """

        # Render the custom grid
        st.markdown(trending_html, unsafe_allow_html=True)

        # ==========================================
        # CATCH THE CLICK EVENT IN PYTHON
        # ==========================================
        # This reads the URL to see which button was clicked
        if "q" in st.query_params:
            query = st.query_params["q"]

        st.markdown("<p style='font-size: 0.95rem; color: #555; margin-bottom: -5px;'><b>Advanced Results Controls</b></p>", unsafe_allow_html=True)
        
        ctrl_col1, ctrl_col2 = st.columns(2, gap="small")
        
        with ctrl_col1:
            max_results = st.slider(
                "Max Results to Display",
                min_value=10, 
                max_value=500, 
                value=50, 
                step=10
            )
            
        with ctrl_col2:
            max_pr_score = 1.0
            if 'ranks' in st.session_state and len(st.session_state['ranks']) > 0:
                max_pr_score = float(max(st.session_state['ranks']))
                max_pr_score = round(max_pr_score + 0.1, 2) 
                
            pr_range = st.slider(
                "PageRank Score Range",
                min_value=0.0, 
                max_value=max_pr_score, 
                value=(0.0, max_pr_score),
                step=0.01
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if query:
            search_word = query.lower().strip()
            # Reset to page 1 if the user searches for a completely new word
            if 'last_query' not in st.session_state or st.session_state['last_query'] != search_word:
                st.session_state['current_page'] = 1
                st.session_state['last_query'] = search_word

            # ⏱️ Timer Start (Searching)
            start_search_time = time.time()

            # ------------------------------------------
            # SEARCH LOGIC ROUTING (HYBRID ENGINE)
            # ------------------------------------------
            if "🤖" in search_mode:
                # ==========================================
                # MODE 1: AI SEMANTIC SEARCH
                # ==========================================
                
                # Convert Session State Ranks to a Dictionary for the AI function
                # Format: {'https://url1.com': 1.25, 'https://url2.com': 0.85}
                ranks_dict = {
                    page: float(score) 
                    for page, score in zip(st.session_state['unique_pages'], st.session_state['ranks'])
                }
                
                # Call the new AI function
                results = ai_semantic_search(
                    query=search_word, 
                    ranks_dict=ranks_dict, 
                    max_results=max_results * 2 # Fetch more for filtering
                )
                
            else:
                # ==========================================
                # MODE 2: EXACT KEYWORD SEARCH
                # ==========================================
                
                # Check if the word is missing from our database
                if search_word not in st.session_state['inverted_index']:
                    
                    # 1. Fuzzy Search: Ask AI for the closest matching word
                    suggestion = get_did_you_mean(
                        query=search_word, 
                        index_keys=list(st.session_state['inverted_index'].keys())
                    )
                    
                    if suggestion:
                        st.markdown(f"""
                        <div style="background-color: #fce8e6; color: #d93025; padding: 12px 15px; border-radius: 8px; margin-bottom: 20px; font-size: 1.05rem;">
                            ❌ No exact match for '<b>{search_word}</b>'. <br>
                            💡 <b>Did you mean:</b> <span style="color: #1a73e8; cursor: pointer; text-decoration: underline;">{suggestion}</span> ?
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Auto-switch the query to the suggested word so results still show up
                        search_word = suggestion 
                    else:
                        st.error(f"No results or close suggestions found for '{search_word}'.")

                # Execute Standard Search
                results = search(
                    query=search_word, 
                    inverted_index=st.session_state['inverted_index'], 
                    unique_pages=st.session_state['unique_pages'], 
                    ranks=st.session_state['ranks']
                )

            # Apply PageRank Range Filter
            filtered_results = [res for res in results if pr_range[0] <= res[1] <= pr_range[1]]
            results = filtered_results[:max_results]

            # ⏱️ Timer Stop (Searching)
            end_search_time = time.time()
            total_search_time = end_search_time - start_search_time

            # SILENT BACKGROUND TRACKER: Log the search analytics
            log_search(search_word, len(results), total_search_time)

            # Display Results
            if results:
                # ------------------------------------------
                # NEW: RESULT BANNER
                # ------------------------------------------
                engine_badge = "🧠 Semantic AI Engine" if "🤖" in search_mode else "⚡ Exact Match Engine"
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); 
                            border-left: 4px solid #1a73e8; 
                            padding: 12px 20px; 
                            border-radius: 4px; 
                            margin-bottom: 20px; 
                            display: flex; 
                            justify-content: space-between; 
                            align-items: center;">
                    <span style="color: #202124; font-size: 0.95rem; font-weight: 500;">
                        Found <b>{len(results)}</b> results in <b>{total_search_time:.4f}s</b>
                    </span>
                    <span style="background-color: #1a73e8; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">
                        {engine_badge}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                # ==========================================
                # EXPORT FEATURE (CSV)
                # ==========================================
                export_data = []
                for rank, (url, score) in enumerate(results):
                    export_data.append({
                        "Rank": rank + 1,
                        "URL": url,
                        "Engine Score (Authority/Relevance)": score
                    })
                    
                df = pd.DataFrame(export_data)
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                
                dl_col1, dl_col2 = st.columns([3, 1])
                with dl_col2:
                    st.download_button(
                        label="📥 Export to CSV",
                        data=csv_bytes,
                        file_name="universe_search_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)
                
                # ==========================================
                # PAGINATION LOGIC
                # ==========================================
                results_per_page = 10
                total_pages = math.ceil(len(results) / results_per_page)
                
                # Make sure current_page doesn't exceed total_pages
                if st.session_state['current_page'] > total_pages:
                    st.session_state['current_page'] = total_pages
                    
                # Calculate start and end indices for slicing the results list
                start_idx = (st.session_state['current_page'] - 1) * results_per_page
                end_idx = start_idx + results_per_page
                
                # Extract only the 10 results for the current page
                current_page_results = results[start_idx:end_idx]
                
                # ==========================================
                # RENDER INDIVIDUAL RESULTS (For Current Page)
                # ==========================================
                # Notice we use current_page_results now, and calculate the actual rank
                for idx, (url, score) in enumerate(current_page_results):
                    actual_rank = start_idx + idx + 1
                    
                    # --- NEW: URL Decoding Logic ---
                    import urllib.parse
                    display_url = urllib.parse.unquote(url)
                    display_title = display_url.split('/')[-1].replace('_', ' ')
                    # -------------------------------
                    
                    full_page_content = st.session_state.get('page_texts', {}).get(url, "No content preview available.")
                    final_snippet = get_best_snippet(full_page_content, search_word)

                    st.markdown(f"""
                    <div style="margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #f1f3f4;">
                        <a href="{url}" target="_blank" style="color: #202124; font-size: 0.85rem; margin-bottom: 4px; text-decoration: none; display: block; opacity: 0.7;">
                            {display_url}
                        </a>
                        <div style="font-size: 1.25rem; font-weight: 400; margin-bottom: 6px; font-family: 'Google Sans', Arial, sans-serif;">
                            <a href="{url}" target="_blank" style="color: #1a0dab; text-decoration: none;">
                                {actual_rank}. {display_title}
                            </a>
                        </div>
                        <div style="font-size: 0.95rem; color: #4d5156; line-height: 1.5; margin-bottom: 6px;">
                            {final_snippet}
                        </div>
                        <div style="font-size: 0.8rem; color: #1a73e8; font-weight: 500;">
                            {'🎯 Final Fused Score:' if "🤖" in search_mode else '📈 PageRank Score:'} {score:.6f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ==========================================
                # PAGINATION BUTTONS (Footer)
                # ==========================================
                st.markdown("<br>", unsafe_allow_html=True)
                pag_col1, pag_col2, pag_col3 = st.columns([1, 2, 1])
                
                with pag_col1:
                    if st.session_state['current_page'] > 1:
                        if st.button("⬅️ Previous Page", use_container_width=True):
                            st.session_state['current_page'] -= 1
                            st.rerun()
                            
                with pag_col2:
                    st.markdown(f"<div style='text-align: center; color: #555; padding-top: 5px;'><b>Page {st.session_state['current_page']} of {total_pages}</b></div>", unsafe_allow_html=True)
                    
                with pag_col3:
                    if st.session_state['current_page'] < total_pages:
                        if st.button("Next Page ➡️", use_container_width=True):
                            st.session_state['current_page'] += 1
                            st.rerun()
                    
            else:
                st.error(f"No results found for '{search_word}'. Try adjusting your query or PageRank filters.")

    # ==========================================
    # TAB 2: EXPAND & CRAWL (The Web Crawler)
    # ==========================================
    with tab_crawl:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. ORIGINAL TITLE & QUOTE DESIGN (Directly in Tab)
        st.markdown("""
            <style>
            .custom-crawler-title {
                font-size: 1.5rem;
                font-weight: 800;
                text-align: center;
                color: #222222;
                line-height: 1.2;
            }
            .custom-crawler-quote {
                font-size: 0.9rem;
                color: #666666;
                text-align: center;
                font-style: italic;
                margin-top: 5px;
                margin-bottom: 25px;
            }
            
            /* 📱 Media Query: */
            @media (max-width: 320px) {
                .custom-crawler-title { font-size: 1.2rem; }
                .custom-crawler-quote { font-size: 0.8rem; }
            }
            </style>
            
            <div class="custom-crawler-title">🕷️ Crawl The Universe</div>
            <div class="custom-crawler-quote">"Define your search universe"</div>
        """, unsafe_allow_html=True)

        # Grid Layout for Input & Controls
        c_col1, c_col2 = st.columns([2, 1], gap="medium")

        with c_col1:
            # 2. ORIGINAL SEED URL LABEL WITH LINK
            st.markdown(
                """
                <div style="font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                    🌱 Enter Seed URLs or 
                    <a href="#" target="_blank" style="color: #1f77b4; text-decoration: none; border-bottom: 1.5px dashed #1f77b4; padding-bottom: 1px; transition: 0.3s;">
                        Choose from here
                    </a>
                    <br>
                    <span style="font-size: 12px; font-weight: normal; color: #7f8c8d; margin-left: 5px;">
                        (one URL per line)
                    </span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            seed_urls_input = st.text_area(
                label="hidden_seed_label", 
                value="https://en.wikipedia.org/wiki/Data_science\nhttps://en.wikipedia.org/wiki/Artificial_intelligence",
                height=150,
                label_visibility="collapsed",
                key="tab_seed_urls"
            )
            
        with c_col2:
            st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 8px;'>⚙️ Crawl Settings</div>", unsafe_allow_html=True)
            use_custom_limit = st.checkbox("🔓 Unlock Custom Limit", key="tab_custom_limit_check")
            
            if use_custom_limit:
                # Pro Mode
                max_pages = st.number_input(
                    "Enter Exact Max Pages:", 
                    min_value=1, 
                    max_value=9_007_199_254_740_991, 
                    value=500, 
                    step=50,
                    key="tab_max_pages_num"
                )
            else:
                # Normal Mode
                max_pages = st.slider(
                    "Max Pages to Crawl:", 
                    min_value=10, 
                    max_value=500, 
                    value=50, 
                    step=10,
                    key="tab_max_pages_slider"
                )
                
        # Centered Button and Terminal
        st.markdown("<br>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])

        with b_col2:
            start_button = st.button("🚀 Start Web Crawler", type="primary", use_container_width=True, key="tab_start_button")
            
        # The Crawling Logic
        if start_button:
            raw_urls = seed_urls_input.split('\n')
            seed_urls = [url.strip() for url in raw_urls if url.strip().startswith("http")]
            
            if not seed_urls:
                st.error("Please enter at least one valid URL starting with http:// or https://")
            else:
                # TERMINAL SETUP
                terminal_box = st.empty() 
                log_data = ["> INITIALIZING MULTI-SEED CRAWLER...\n"] 
                terminal_box.code(log_data[0], language='bash')
                
                def update_ui(msg):
                    log_data[0] += "> CRAWLING: " + msg + "\n"
                    lines = log_data[0].split('\n')
                    if len(lines) > 8: 
                        log_data[0] = '\n'.join(lines[-8:])
                    terminal_box.code(log_data[0], language='bash')

                start_crawl_time = time.time()
                web_graph, inverted_index, page_texts = build_web_graph(seed_urls, max_pages=max_pages, ui_callback=update_ui)
                
                if web_graph:
                    unique_pages, ranks = calculate_pagerank(web_graph)
                    end_crawl_time = time.time()
                    total_crawl_time = end_crawl_time - start_crawl_time 

                    ranks_dict = {page: float(score) for page, score in zip(unique_pages, ranks)}
                    save_crawled_data(web_graph, inverted_index, page_texts, ranks_dict)
                    
                    st.session_state['inverted_index'] = inverted_index
                    st.session_state['unique_pages'] = unique_pages
                    st.session_state['ranks'] = ranks
                    st.session_state['page_texts'] = page_texts
                    st.session_state['web_graph'] = web_graph
                    st.session_state['is_crawled'] = True
                    
                    log_data[0] += f"\n> ✅ MATRIX GENERATED.\n> ✅ PAGERANK CALCULATED in {total_crawl_time:.2f}s."
                    terminal_box.code(log_data[0], language='bash')
                    st.success(f"✅ Indexed {len(unique_pages)} pages in {total_crawl_time:.2f} seconds!")
                else:
                    st.error("⚠️ Failed to crawl. The target websites might be blocking bots.")
                        
    # ==========================================
    # TAB 2: DATA VISUALIZATION DASHBOARD
    # ==========================================
    with tab_insights:
        st.markdown('<h4 class="analytics-dashboard-title">Network Analytics Dashboard</h4>', unsafe_allow_html=True)
        
        unique_pages = st.session_state['unique_pages']
        ranks = st.session_state['ranks']
        web_graph = st.session_state['web_graph']
        inverted_index = st.session_state['inverted_index']
        
        # 1. Top Level KPI Metrics
        # ==========================================
        # CALCULATE METRICS
        # ==========================================
        total_pages = len(unique_pages)
        total_words = len(inverted_index)
        max_pr_score = float(max(ranks)) if len(ranks) > 0 else 0.0
        total_links = sum(len(links) for links in web_graph.values())
        avg_links = total_links / total_pages if total_pages > 0 else 0
        
        # ==========================================
        # RENDER PREMIUM METRIC CARDS
        # ==========================================
        st.markdown(f"""
        <style>
        .metric-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            padding: 20px 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            border: 1px solid #e9ecef;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }}
        .metric-icon {{
            font-size: 26px;
            margin-bottom: 12px;
        }}
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a0dab;
            margin-bottom: 5px;
            font-family: 'Google Sans', Arial, sans-serif;
            line-height: 1.2;
        }}
        .metric-label {{
            font-size: 0.8rem;
            color: #5f6368;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Mobile View: 2x2 Grid setup */
        @media (max-width: 768px) {{
            .metric-container {{
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }}
            .metric-value {{ 
                font-size: 1.4rem; 
            }}
            .metric-label {{ 
                font-size: 0.7rem; 
                letter-spacing: 0px;
            }}
            .metric-card {{ 
                padding: 15px 10px; 
            }}
            .metric-icon {{
                font-size: 22px;
                margin-bottom: 8px;
            }}
        }}
        </style>

        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-icon">📄</div>
                <div class="metric-value">{total_pages:,}</div>
                <div class="metric-label">Total Indexed Pages</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📚</div>
                <div class="metric-value">{total_words:,}</div>
                <div class="metric-label">Total Vocabulary</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">⭐</div>
                <div class="metric-value">{max_pr_score:.4f}</div>
                <div class="metric-label">Highest Authority</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🔗</div>
                <div class="metric-value">{avg_links:.1f}</div>
                <div class="metric-label">Avg Links per Page</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        # Create a layout for charts
        chart_col1, chart_col2 = st.columns(2)
        
        # 2. Bar Chart: Top 10 High Authority Pages
        with chart_col1:
            st.markdown("<p style='font-weight: 500;'>🏆 Top 10 Authority Pages (PageRank)</p>", unsafe_allow_html=True)
            
            # Combine URLs and Ranks, sort them, and take top 10
            ranked_pages = sorted(zip(unique_pages, ranks), key=lambda x: x[1], reverse=True)[:10]
            
            # ==========================================
            # Clean URLs for better display on the chart
            # ==========================================
            import urllib.parse
            
            display_urls = []
            for url, score in ranked_pages:
                raw_title = url.split('/')[-1]
                clean_title = urllib.parse.unquote(raw_title).replace('_', ' ')
                
                if len(clean_title) > 25:
                    final_title = clean_title[:25] + '...'
                else:
                    final_title = clean_title
                    
                display_urls.append(final_title)

            scores = [score for url, score in ranked_pages]
            
            df_top = pd.DataFrame({'Page': display_urls, 'PageRank': scores})
            
            fig_bar = px.bar(
                df_top, 
                x='PageRank', 
                y='Page', 
                orientation='h',
                color='PageRank',
                color_continuous_scale='Viridis'
            )
            fig_bar.update_layout(
                margin=dict(l=0, r=0, t=30, b=50), 
                yaxis={'categoryorder': 'total ascending'},
                coloraxis_colorbar=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    title="" 
                )
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # 3. Pie Chart: Domain Extension Distribution
        with chart_col2:
            st.markdown("<p style='font-weight: 500;'>🌍 Network Distribution (Top Level Domains)</p>", unsafe_allow_html=True)
            
            # Extract domain extensions (like .com, .org, .edu) from all indexed URLs
            extensions = []
            for url in unique_pages:
                netloc = urlparse(url).netloc
                parts = netloc.split('.')
                if len(parts) > 1:
                    extensions.append('.' + parts[-1])
                else:
                    extensions.append('Other')
            
            df_ext = pd.DataFrame({'Extension': extensions})
            ext_counts = df_ext['Extension'].value_counts().reset_index()
            ext_counts.columns = ['Extension', 'Count']
            
            # Keep top 5 extensions, group the rest as 'Other'
            if len(ext_counts) > 5:
                top_5 = ext_counts.head(5)
                other_count = ext_counts['Count'][5:].sum()
                top_5.loc[len(top_5)] = ['Other', other_count]
                ext_counts = top_5
                
            fig_pie = px.pie(
                ext_counts, 
                values='Count', 
                names='Extension', 
                hole=0.4, 
                color_discrete_sequence=px.colors.sequential.Teal
            )
            
            fig_pie.update_layout(
                margin=dict(l=0, r=0, t=30, b=50),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        # Injecting a native browser print button using HTML/JS
        components.html(
            """
            <button onclick="window.parent.print()" style="
                background-color: #2e6fdf; 
                border: none;
                color: white; 
                padding: 12px 24px; 
                text-align: center; 
                text-decoration: none; 
                display: block; 
                font-size: 16px; 
                margin: 0 auto; 
                cursor: pointer; 
                border-radius: 6px;
                font-family: sans-serif;
                font-weight: 600;
                width: 100%;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                🖨️ Export Dashboard Summary (PDF)
            </button>
            """,
            height=70
        )

    # ==========================================
    # TAB 3: ABOUT THE ENGINE
    # ==========================================
    with tab_about:
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

    # ==========================================
    # TAB 4: ABOUT ME
    # ==========================================
    with tab_me:
        st.markdown("""
        ## 👨‍💻 Meet the Developer
        
        Welcome! I am **Lokendra Kushwaha**, the architect and developer behind the Universe Crawler.

        ---

        ### 🛠️ Technical Arsenal
        * **Languages:** Python, SQL, JavaScript, HTML/CSS
        * **Frameworks & Libraries:** Streamlit, Pandas, BeautifulSoup, Sentence-Transformers, TheFuzz
        * **Core Concepts:** Mathematics, Data Structures & Algorithms, Natural Language Processing (NLP), Vector Databases (ChromaDB), Multithreaded Processing

        ### 🎯 The Vision
        I engineered this search engine entirely from scratch to showcase my capability in building complex, data-heavy architectures. Instead of relying on plug-and-play APIs, I focused on implementing the core mathematics of PageRank and leveraging advanced Data Structures and Algorithms to build a robust foundation. This project reflects my true ambition: not just integrating existing AI tools, but engineering intelligent, locally-driven semantic systems and high-performance backends from the ground up.

        ---

        ### 📫 Let's Connect
        * 💼 **LinkedIn:** www.linkedin.com/in/the-lokendra-kushwaha
        * 🐙 **GitHub:** https://github.com/lokendra-kushwaha
        * ✉️ **Email:** thelokendrakushwaha@gmail.com
        
        <br>
        """, unsafe_allow_html=True)

    # ==========================================
    # TAB 5: ADMIN DASHBOARD
    # ==========================================
    with tab_admin:
        st.markdown("### ⚙️ Admin Control Center")
        
        admin_password = st.text_input(
            "Enter Admin Key to unlock analytics:", 
            type="password", 
            help="Restricted area for system administrators only."
        )
        
        if admin_password == "lokendra":
            st.success("🔓 Access Granted! Welcome to the Command Center.")
            
            st.markdown("""
            <div style="margin-top: 10px; margin-bottom: 25px; padding-bottom: 12px; border-bottom: 2px solid #f1f3f4;">
                <h3 style="color: #202124; font-family: 'Google Sans', Arial, sans-serif; font-size: 1.5rem; font-weight: 600; margin: 0; display: flex; align-items: center; gap: 10px;">
                    <span style="background: #fce8e6; color: #d93025; padding: 6px 12px; border-radius: 8px; font-size: 1.2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        📊
                    </span> 
                    System Analytics
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Fetch LIVE data from the database
            total_searches, avg_time = get_admin_metrics()
            total_indexed = len(st.session_state.get('unique_pages', []))
            
            # Render Admin Metric Cards
            st.markdown(f"""
            <style>
            .admin-metric-container {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }}
            .admin-metric-card {{
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 12px;
                padding: 20px 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.04);
                border: 1px solid #e9ecef;
                text-align: center;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .admin-metric-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            }}
            .admin-metric-icon {{
                font-size: 26px;
                margin-bottom: 12px;
            }}
            .admin-metric-value {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #d93025; /* Admin Command Center Red */
                margin-bottom: 5px;
                font-family: 'Google Sans', Arial, sans-serif;
                line-height: 1.2;
            }}
            .admin-metric-label {{
                font-size: 0.8rem;
                color: #5f6368;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            /* Mobile View: Stack vertically for 3 items */
            @media (max-width: 768px) {{
                .admin-metric-container {{
                    grid-template-columns: repeat(1, 1fr);
                    gap: 12px;
                }}
                .admin-metric-value {{ 
                    font-size: 1.5rem; 
                }}
                .admin-metric-card {{ 
                    padding: 15px 10px; 
                }}
            }}
            </style>
    
            <div class="admin-metric-container">
                <div class="admin-metric-card">
                    <div class="admin-metric-icon">🔍</div>
                    <div class="admin-metric-value">{total_searches:,}</div>
                    <div class="admin-metric-label">Total Searches Executed</div>
                </div>
                <div class="admin-metric-card">
                    <div class="admin-metric-icon">⚡</div>
                    <div class="admin-metric-value">{avg_time:.5f}s</div>
                    <div class="admin-metric-label">Avg. Search Time</div>
                </div>
                <div class="admin-metric-card">
                    <div class="admin-metric-icon">🗄️</div>
                    <div class="admin-metric-value">{total_indexed:,}</div>
                    <div class="admin-metric-label">Total Pages Indexed</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
                
            # ==========================================
            # DASHBOARD VISUALIZATIONS
            # ==========================================
            st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            st.markdown("#### 🔍 Search Query Analytics")
            
            # Create two columns for the data tables
            table_col1, table_col2 = st.columns(2, gap="large")
            
            with table_col1:
                st.markdown("<p style='color: #1a73e8; font-weight: 600;'>🏆 Top 10 Most Searched Queries</p>", unsafe_allow_html=True)
                top_queries_df = get_top_queries()
                
                if not top_queries_df.empty:
                    # hide_index=True keeps the table looking clean like a professional dashboard
                    st.dataframe(top_queries_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No search data available yet. Start searching to generate logs.")
                    
            with table_col2:
                st.markdown("<p style='color: #d93025; font-weight: 600;'>⚠️ Zero-Result Queries (Content Gaps)</p>", unsafe_allow_html=True)
                zero_queries_df = get_zero_result_queries()
                
                if not zero_queries_df.empty:
                    st.dataframe(zero_queries_df, use_container_width=True, hide_index=True)
                    st.caption("Tip: Crawl pages related to these keywords to improve your engine.")
                else:
                    st.success("Great! No failed searches recorded so far.")
                
        elif admin_password != "":
            st.error("❌ Invalid Key. Access Denied.")

        else:
            st.warning("🔒 This area is restricted to system administrators. Please enter the key.")


else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.info("👈 Open the sidebar menu and start the crawler to build your index.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    img_col1, img_col2, img_col3 = st.columns(3, gap="medium")
    
    with img_col1:
        st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=500&q=80", use_container_width=True)
        
    with img_col2:
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=500&q=80", use_container_width=True)
        
    with img_col3:
        st.image("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=500&q=80", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    feat1, feat2, feat3 = st.columns(3, gap="medium")
    
    with feat1:
        st.success("🕷️ **Dynamic Crawling**\n\nBuilds a comprehensive Web Graph in real-time by traversing live URL routes.")
    with feat2:
        st.warning("🧮 **Markov Matrix Math**\n\nPrevents underflow while calculating precise PageRank authority via NumPy.")
    with feat3:
        st.info("⚡ **Microsecond Search**\n\nInstantly retrieves matching nodes using a custom Hashed Inverted Index.")

    st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# 6. FOOTER
# ==========================================
footer_html = """
<style>
/* 1. Add padding to Streamlit's main block so the last content doesn't hide behind the footer */
.block-container {
    padding-bottom: 100px !important;
}

/* 2. Make the footer stick to the bottom */
.premium-footer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 100% !important;
    z-index: 9999 !important; /* Keeps footer on top of all other elements */
    background-color: #ffffff !important; /* Solid white background is required */
    text-align: center;
    padding-top: 12px;
    padding-bottom: 15px;
    border-top: 1px solid #e8eaed; 
    box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.05); /* Sleek shadow above the footer */
    color: #5f6368; 
    font-size: 0.85rem;
    font-family: 'Inter', sans-serif;
}
.premium-footer p {
    margin: 5px 0px !important; 
    line-height: 1.5 !important;
}
.premium-footer a {
    color: #1a73e8; 
    text-decoration: none;
    font-weight: 600;
}
.premium-footer a:hover {
    text-decoration: underline;
    color: #1557b0;
}
.footer-heart {
    color: #ea4335; 
    font-size: 0.95rem;
}
.footer-title {
    font-weight: 700;
    color: #202124;
}
</style>

<div class="premium-footer">
    <p>Engineered with <span class="footer-heart">❤️</span> by <span class="footer-title">Lokendra Kushwaha</span></p>
    <p>© 2026 The Universe Crawler Project | <a href="#" target="_blank">GitHub</a> • <a href="#" target="_blank">LinkedIn</a> • <a href="#" target="_blank">Portfolio</a></p>
</div>
"""

# Render the sticky footer
st.markdown(footer_html, unsafe_allow_html=True)