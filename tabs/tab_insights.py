import streamlit as st
from frontend.tab_ui_components import render_insight_metrics_ui, render_print_button_ui
from frontend.charts import render_top_authority_bar_chart, render_domain_pie_chart

def render_insights_tab():
    """Main function to render the Data Visualization Dashboard tab"""
    st.markdown('<h4 class="analytics-dashboard-title">Network Analytics Dashboard</h4>', unsafe_allow_html=True)
    
    unique_pages = st.session_state.get('unique_pages', [])
    ranks = st.session_state.get('ranks', [])
    web_graph = st.session_state.get('web_graph', {})
    inverted_index = st.session_state.get('inverted_index', {})
    
    # ==========================================
    # CALCULATE METRICS
    # ==========================================
    total_pages = len(unique_pages)
    total_words = len(inverted_index)
    max_pr_score = float(max(ranks)) if len(ranks) > 0 else 0.0
    total_links = sum(len(links) for links in web_graph.values())
    avg_links = total_links / total_pages if total_pages > 0 else 0
    
    # Call UI component for top metrics
    render_insight_metrics_ui(total_pages, total_words, max_pr_score, avg_links)
    
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    # Create a layout for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        render_top_authority_bar_chart(unique_pages, ranks)
            
    with chart_col2:
        render_domain_pie_chart(unique_pages)
    
    st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    # Call UI component for print button
    render_print_button_ui()