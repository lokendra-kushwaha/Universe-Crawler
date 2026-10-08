import streamlit as st
from frontend.tab_ui_components import render_admin_system_analytics_header, render_admin_metrics_ui
from backend.db_manager import get_admin_metrics, get_top_queries, get_zero_result_queries

def render_admin_tab():
    """
    Main function to render the Admin Dashboard.
    Database functions are passed as arguments to avoid import errors during refactoring.
    """
    st.markdown("### ⚙️ Admin Control Center")
    
    admin_password = st.text_input(
        "Enter Admin Key to unlock analytics:", 
        type="password", 
        help="Restricted area for system administrators only."
    )
    
    if admin_password == "lokendra":
        st.success("🔓 Access Granted! Welcome to the Command Center.")
        
        render_admin_system_analytics_header()
        
        # Fetch LIVE data from the database using the passed functions
        total_searches, avg_time = get_admin_metrics()
        total_indexed = len(st.session_state.get('unique_pages', []))
        
        # Call the UI module to render the metric cards
        render_admin_metrics_ui(total_searches, avg_time, total_indexed)
            
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