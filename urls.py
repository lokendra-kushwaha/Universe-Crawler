import streamlit as st

from frontend.header_ui import (
    render_header_and_global_css, 
    render_custom_responsive_css
)

from frontend.footer_ui import render_footer

st.set_page_config(page_title="Safe URLs Directory", page_icon="🌐", layout="centered")

# ==========================================
# UI: MAIN AREA & GLOBAL STYLES
# ==========================================
render_header_and_global_css()
render_custom_responsive_css()

# ==========================================
# CUSTOM CSS FOR PREMIUM RESPONSIVE DESIGN
# ==========================================
st.markdown("""
    <style>
    /* 1. HIDE STREAMLIT DEFAULT HEADER & FOOTER */
    [data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    
    /* 2. ADJUST MAIN CONTAINER PADDING */
    .block-container {
        padding-top: 75px !important;
        padding-bottom: 3rem !important;
        max-width: 800px;
    }
    
    /* 3. PREMIUM TYPOGRAPHY FOR TITLE */
    .directory-title {
        text-align: center;
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        font-weight: 800;
        color: #1a73e8; /* Blue */
        margin-top: 45px;
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
    }
    .directory-subtitle {
        text-align: center;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        color: #5f6368;
        margin-bottom: 30px;
    }

    /* 4. PREMIUM URL BOX DESIGN */
    .custom-url-box {
        background: linear-gradient(145deg, #ffffff, #f8faff);
        border-radius: 12px;
        padding: 25px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 15px;
        color: #202124;
        line-height: 1.9;
        border: 1.5px solid #e8eaed;
        box-shadow: 0 8px 24px rgba(26, 115, 232, 0.05);
        overflow-x: auto;
        transition: all 0.3s ease;
    }
    
    .custom-url-box:hover {
        box-shadow: 0 12px 32px rgba(26, 115, 232, 0.12);
        border-color: #d2e3fc;
    }

    /* URL Highlight Effect */
    .url-line {
        display: block;
        padding: 6px 10px;
        border-radius: 6px;
        transition: background-color 0.2s;
        border-bottom: 1px dashed #e8eaed;
    }
    .url-line:hover {
        background-color: #e8f0fe;
        color: #1557b0;
        font-weight: 600;
    }
    .url-line:last-child {
        border-bottom: none;
    }

    /* 5. DARK MODE ADAPTATION */
    @media (prefers-color-scheme: dark) {
        .directory-title { color: #8ab4f8; }
        .directory-subtitle { color: #9aa0a6; }
        .custom-url-box {
            background: linear-gradient(145deg, #202124, #282a2d);
            color: #e8eaed;
            border: 1px solid #3c4043;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }
        .custom-url-box:hover {
            border-color: #5f6368;
        }
        .url-line { border-bottom: 1px dashed #3c4043; }
        .url-line:hover {
            background-color: #303134;
            color: #8ab4f8;
        }
    }

    /* 6. MOBILE RESPONSIVENESS */
    @media (max-width: 600px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .custom-url-box {
            padding: 15px;
            font-size: 13px; /* Smaller font for mobile */
        }
        .url-line {
            white-space: nowrap; /* Prevent messy wrapping on small screens */
            padding: 8px 5px;
        }
        .directory-title {
            font-size: 1.5rem !important; 
            white-space: nowrap !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE CONTENT
# ==========================================
st.markdown('<div class="directory-title">🌐 Safe URLs Directory</div>', unsafe_allow_html=True)
st.markdown('<div class="directory-subtitle">Copy these verified URLs and paste them into the main crawler engine to safely expand your network database.</div>', unsafe_allow_html=True)

try:
    with open("safe_urls.txt", "r") as f:
        urls_data = f.read().splitlines()
        
    # Filter out empty lines to keep the list clean
    urls_data = [url.strip() for url in urls_data if url.strip()]
    
    # Format each URL into a beautiful hoverable line
    formatted_html = ""
    for url in urls_data:
        formatted_html += f'<span class="url-line">{url}</span>'
        
    st.markdown(f'<div class="custom-url-box">{formatted_html}</div>', unsafe_allow_html=True)
    
except FileNotFoundError:
    st.error("⚠️ The file 'safe_urls.txt' was not found. Please create it in the main directory.")


# ==========================================
# FOOTER
# ==========================================
render_footer()