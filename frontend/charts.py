import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
from urllib.parse import urlparse

pd.options.mode.chained_assignment = None

def render_top_authority_bar_chart(unique_pages, ranks):
    """Renders the Top 10 High Authority Pages Bar Chart"""
    st.markdown("<p style='font-weight: 500;'>🏆 Top 10 Authority Pages (PageRank)</p>", unsafe_allow_html=True)
    
    # Combine URLs and Ranks, sort them, and take top 10
    ranked_pages = sorted(zip(unique_pages, ranks), key=lambda x: x[1], reverse=True)[:10]
    
    # Clean URLs for better display on the chart
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


def render_domain_pie_chart(unique_pages):
    """Renders the Domain Extension Distribution Pie Chart"""
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
        top_5 = ext_counts.head(5).copy()
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