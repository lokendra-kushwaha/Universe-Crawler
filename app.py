import streamlit as st

from frontend.loader_ui import render_custom_loader
loader = render_custom_loader()

from backend.db_manager import (
    init_db, initialize_logs_table, load_database
)

from frontend.header_ui import (
    render_header_and_global_css, 
    render_custom_responsive_css
)

from tabs.expander import render_crawler_expander

from tabs.tab_search import render_search_tab
from tabs.tab_crawl import render_crawl_tab
from tabs.tab_insights import render_insights_tab
from tabs.tab_engine import render_about_engine
from tabs.tab_me import render_me_tab
from tabs.tab_admin import render_admin_tab

from frontend.footer_ui import render_footer


# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Universe Crawler", page_icon="🌌", layout="wide")

# ==========================================
# SESSION STATE INITIALIZATION (MAMORY)
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
    
    if isinstance(ranks, dict) and unique_pages:
        st.session_state['ranks'] = [ranks.get(page, 0.0) for page in unique_pages]
    else:
        st.session_state['ranks'] = ranks
        
    # Automatically activate the search UI and dashboard if data already exists
    if web_graph:
        st.session_state['is_crawled'] = True
    else:
        st.session_state['is_crawled'] = False

loader.empty()

# ==========================================
# CRAWLER CONTROL PANEL (Hidden in Expander)
# ==========================================
render_crawler_expander()


# ==========================================
# UI: MAIN AREA & GLOBAL STYLES
# ==========================================
render_header_and_global_css()
render_custom_responsive_css()


# ==========================================
# TAB SECTION
# ==========================================
if st.session_state.get('is_crawled', False):
    # Display statistics of the current database
    st.info(f"📊 **Database Status:** {len(st.session_state['unique_pages'])} total URLs indexed and ranked.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Creating tabs
    tab_search, tab_crawl, tab_insights, tab_engine, tab_me, tab_admin = st.tabs([
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
        render_search_tab()

    # ==========================================
    # TAB 2: EXPAND & CRAWL (The Web Crawler)
    # ==========================================
    with tab_crawl:
        render_crawl_tab()
                 
    # ==========================================
    # TAB 3: DATA VISUALIZATION DASHBOARD
    # ==========================================
    with tab_insights:
        render_insights_tab()

    # ==========================================
    # TAB 4: ABOUT THE ENGINE
    # ==========================================
    with tab_engine:
        render_about_engine()

    # ==========================================
    # TAB 5: MEET THE DEVELOPER
    # ==========================================
    with tab_me:
        render_me_tab()

    # ==========================================
    # TAB 6: ADMIN DASHBOARD
    # ==========================================
    with tab_admin:
        render_admin_tab()


else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
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
        st.warning("🧮 **Markov Matrix Math**\n\nPrevents underflow while calculating precise PageRank authority.")
    with feat3:
        st.info("⚡ **Microsecond Search**\n\nInstantly retrieves matching nodes using a custom Hashed Inverted Index.")

    st.markdown("<br><br>", unsafe_allow_html=True)


# ==========================================
# FOOTER
# ==========================================
render_footer()