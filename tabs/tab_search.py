import streamlit as st
from .voice_engine import inject_voice_search
import time
import math
import pandas as pd
import urllib.parse

from frontend.tab_ui_components import (
    render_search_mode_toggle_ui, render_search_header_ui, 
    render_trending_searches_ui, render_fuzzy_suggestion_ui,
    render_search_stats_banner_ui, render_individual_result_ui,
    render_premium_export_divider
)
from backend.db_manager import log_search
from backend.search_engine import (
    ai_semantic_search, get_did_you_mean, search, get_best_snippet
)

def render_search_tab():
    """Main function for the Search Engine Tab"""
    render_search_header_ui()
    
    # ------------------------------------------
    # NEW: PREMIUM SEARCH MODE TOGGLE
    # ------------------------------------------
    render_search_mode_toggle_ui()
    search_mode = st.radio(
        "Select Search Engine Mode:",
        ["🧠 AI Semantic (Meaning & Context)", "🎯 Exact Keyword (Speed & Precision)"],
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
        placeholder="Type your query...",
        label_visibility="collapsed",
        key="my_search_key",
        on_change=sync_to_url
    )

    inject_voice_search()

    render_trending_searches_ui()

    # ==========================================
    # CATCH THE CLICK EVENT IN PYTHON
    # ==========================================
    if "q" in st.query_params:
        query = st.query_params["q"]

    # Use st.expander instead of st.sidebar to protect custom CSS layout
    with st.expander("⚙️ Engine Settings", expanded=False):
        
        # Initialize SafeSearch state if it doesn't exist
        if 'safesearch' not in st.session_state:
            st.session_state['safesearch'] = True
            
        safe_search_toggle = st.toggle(
            "🛡️ SafeSearch", 
            value=st.session_state['safesearch'],
            help="Hide 18+ explicit content from search results"
        )
        st.session_state['safesearch'] = safe_search_toggle
        
        # Dynamic warning inside the expander
        if not st.session_state['safesearch']:
            st.markdown("<p style='color: #ff4b4b; font-size: 0.85rem; margin-top: 5px;'>⚠️ Unrestricted Mode Active. Explicit content may appear.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.95rem; color: #555; margin-bottom: -5px;'><b>Advanced Results Controls</b></p>", unsafe_allow_html=True)
    
    ctrl_col1, ctrl_col2 = st.columns(2, gap="small")
    
    with ctrl_col1:
        max_results = st.slider(
            "Max Results to Display",
            min_value=10, max_value=500, value=50, step=10
        )
        
    with ctrl_col2:
        max_pr_score = 1.0
        if 'ranks' in st.session_state and len(st.session_state['ranks']) > 0:
            max_pr_score = float(max(st.session_state['ranks']))
            max_pr_score = round(max_pr_score + 0.1, 2) 
            
        pr_range = st.slider(
            "PageRank Score Range",
            min_value=0.0, max_value=max_pr_score, value=(0.0, max_pr_score), step=0.01
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if query:
        search_word = query.lower().strip()
        # Reset to page 1 if the user searches for a completely new word
        if 'last_query' not in st.session_state or st.session_state['last_query'] != search_word:
            if 'current_page' not in st.session_state:
                st.session_state['current_page'] = 1
            else:
                st.session_state['current_page'] = 1
            st.session_state['last_query'] = search_word

        # ⏱️ Timer Start (Searching)
        start_search_time = time.time()

        # ------------------------------------------
        # SEARCH LOGIC ROUTING (HYBRID ENGINE)
        # ------------------------------------------
        is_ai_mode = "🧠" in search_mode
        
        if is_ai_mode:
            ranks_dict = {
                page: float(score) 
                for page, score in zip(st.session_state.get('unique_pages', []), st.session_state.get('ranks', []))
            }
            results = ai_semantic_search(
                query=search_word, 
                ranks_dict=ranks_dict, 
                max_results=max_results * 2 
            )
            
        else:
            if search_word not in st.session_state.get('inverted_index', {}):
                suggestion = get_did_you_mean(
                    query=search_word, 
                    index_keys=list(st.session_state.get('inverted_index', {}).keys())
                )
                
                if suggestion:
                    render_fuzzy_suggestion_ui(search_word, suggestion)
                    search_word = suggestion 
                else:
                    st.error(f"No results or close suggestions found for '{search_word}'.")

            results = search(
                query=search_word, 
                inverted_index=st.session_state.get('inverted_index', {}), 
                unique_pages=st.session_state.get('unique_pages', []), 
                ranks=st.session_state.get('ranks', [])
            )

        # Apply PageRank Range Filter
        filtered_results = [res for res in results if pr_range[0] <= res[1] <= pr_range[1]]
        results = filtered_results[:max_results]

        # ⏱️ Timer Stop (Searching)
        end_search_time = time.time()
        total_search_time = end_search_time - start_search_time

        # SILENT BACKGROUND TRACKER
        log_search(search_word, len(results), total_search_time)

        # Display Results
        if results:
            engine_badge = "🧠 Semantic AI Engine" if is_ai_mode else "⚡ Exact Match Engine"
            render_search_stats_banner_ui(len(results), total_search_time, engine_badge)

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
            
            render_premium_export_divider()
            
            # ==========================================
            # PAGINATION LOGIC
            # ==========================================
            results_per_page = 10
            total_pages = math.ceil(len(results) / results_per_page)
            
            if 'current_page' not in st.session_state:
                st.session_state['current_page'] = 1
                
            if st.session_state['current_page'] > total_pages and total_pages > 0:
                st.session_state['current_page'] = total_pages
                
            start_idx = (st.session_state['current_page'] - 1) * results_per_page
            end_idx = start_idx + results_per_page
            
            current_page_results = results[start_idx:end_idx]
            
            # ==========================================
            # RENDER INDIVIDUAL RESULTS
            # ==========================================
            for idx, (url, score) in enumerate(current_page_results):
                actual_rank = start_idx + idx + 1
                
                display_url = urllib.parse.unquote(url)
                display_title = display_url.split('/')[-1].replace('_', ' ')
                
                full_page_content = st.session_state.get('page_texts', {}).get(url, "No content preview available.")
                final_snippet = get_best_snippet(full_page_content, search_word)

                render_individual_result_ui(
                    url=url, display_url=display_url, actual_rank=actual_rank, 
                    display_title=display_title, final_snippet=final_snippet, 
                    score=score, is_ai_mode=is_ai_mode
                )
            
            # ==========================================
            # PAGINATION BUTTONS (Footer)
            # ==========================================
            pag_col1, pag_col2, pag_col3 = st.columns([1, 2, 1])
            
            with pag_col1:
                if st.session_state['current_page'] > 1:
                    if st.button("⬅️ Previous Page", use_container_width=True):
                        st.session_state['current_page'] -= 1
                        st.rerun()
                        
            with pag_col2:
                if total_pages > 0:
                    st.markdown(f"<div style='text-align: center; color: #555; padding-top: 5px;'><b>Page {st.session_state['current_page']} of {total_pages}</b></div>", unsafe_allow_html=True)
                
            with pag_col3:
                if st.session_state['current_page'] < total_pages:
                    if st.button("Next Page ➡️", use_container_width=True):
                        st.session_state['current_page'] += 1
                        st.rerun()
                
        else:
            # Only show the filter error IF the keyword is actually valid (exists in the index)
            # This prevents double-warnings for completely invalid/garbage queries
            if search_word in st.session_state.get('inverted_index', {}):
                st.error(f"No results found for '{search_word}'. Try adjusting your PageRank filters or check Max Results.")
