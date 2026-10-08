import streamlit as st
import time
from frontend.expander_ui import render_expander_css_ui, render_expander_seed_label_ui

from backend.crawler import build_web_graph
from backend.page_rank import calculate_pagerank
from backend.db_manager import save_crawled_data

def render_crawler_expander():
    """
    Main function to render the VIP Crawler Control Panel Expander.
    """
    with st.expander("🚀 Help Grow the Universe (Index New Websites)", expanded=False):
        
        # 1. ORIGINAL TITLE & QUOTE DESIGN
        render_expander_css_ui()

        # Grid Layout for Input & Controls
        c_col1, c_col2 = st.columns([2, 1], gap="medium")

        with c_col1:
            # 2. ORIGINAL SEED URL LABEL WITH LINK
            render_expander_seed_label_ui()
            
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