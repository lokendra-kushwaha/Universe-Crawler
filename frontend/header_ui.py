import streamlit as st

def render_header_and_global_css():
    """
    Renders the global CSS overrides, responsive layout rules, 
    and the sticky main header for the application.
    """
    st.markdown("""
    <style>
    /* ========================================= */
    /* 1. GLOBAL & STREAMLIT OVERRIDES           */
    /* ========================================= */
    
    /* Make Streamlit's default top menu transparent */
    [data-testid="stHeader"] {
        display: none !important;
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
        padding-top: 20px; 
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
            padding-top: 20px; 
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
            padding-top: 120px !important; 
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
            font-size: 1.4rem !important; /* Isko kam karke 1.1rem ya 1.2rem kar dena agar fir bhi na aaye */
            line-height: 1.2 !important;
            margin-top: 10px !important;
        }

        /* ### (Heading 3) ko target karne ke liye */
        div[data-testid="stMarkdownContainer"] h3 {
            font-size: 1.1rem !important; /* Sub-headings ke liye */
            line-height: 1.2 !important;
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
    /* MAIN PRIMARY BUTTON UPGRADE (BLUE THEME)  */
    /* ========================================= */
        button[kind="primary"] {
            background: linear-gradient(135deg, #1a73e8, #0d47a1) !important;
            border: none !important;
            border-radius: 8px !important;
            color: white !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 10px rgba(26, 115, 232, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        button[kind="primary"]:hover {
            box-shadow: 0 6px 14px rgba(26, 115, 232, 0.4) !important;
            transform: translateY(-2px) !important;
            background: linear-gradient(135deg, #1557b0, #0a3880) !important;
            color: white !important;
        }

        /* ========================================= */
        /* PREMIUM UI UPGRADES (STATUS & BUTTON)     */
        /* ========================================= */

        /* ======================================================== */
        /* UNIFIED DATABASE STATUS BOX (stAlert / st.info)          */
        /* ======================================================== */

        /* 1. Light Mode (Your Original Premium Dashboard Design & Layout) */
        div[data-testid="stAlert"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-left: 4px solid #1a73e8 !important; /* Premium Google Blue accent */
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
            padding: 15px 20px !important;
            margin-top: -15px !important; /* Your custom layout pull-up trick */
            transition: all 0.3s ease-in-out !important;
        }

        div[data-testid="stAlert"] * {
            color: #202124 !important;
            font-weight: 500 !important;
        }
        
        div[data-testid="stAlert"] strong {
            color: #1a73e8 !important; /* Match accent color for bold text */
            font-weight: 800 !important;
        }

        /* 2. Auto Dark Mode Overrides (Cyber-Glassmorphism) */
        @media (prefers-color-scheme: dark) {
            
            div[data-testid="stAlert"] {
                background-color: rgba(30, 41, 59, 0.9) !important; /* Dark glass */
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-left: 4px solid #00f2fe !important; /* Neon Blue accent */
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
            }
            
            div[data-testid="stAlert"] * {
                color: #f8fafc !important; /* Soft white text */
                font-weight: 500 !important;
            }
            
            div[data-testid="stAlert"] strong {
                color: #00f2fe !important; /* Glowing Neon Blue text for emphasis */
                text-shadow: 0px 0px 8px rgba(0, 242, 254, 0.4) !important;
                font-weight: 800 !important;
            }
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

    /* ======================================================== */
    /* DYNAMIC PREMIUM DARK MODE (BRUTAL OVERRIDES)             */
    /* ======================================================== */
    @media (prefers-color-scheme: dark) {
        
        /* 1. Main Background */
        .stApp, .main { 
            background-color: #0a0f19 !important; 
        }
        
        /* 2. Frosted Glass Header */
        .fixed-main-header {
            background: rgba(10, 15, 25, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* 3. Fixed Title */
        .sticky-title {
            color: #00f2fe !important;
            text-shadow: 0px 2px 15px rgba(0, 242, 254, 0.5) !important;
            background: none !important;
            -webkit-text-fill-color: initial !important;
        }
        .sticky-subtitle { 
            color: #e2e8f0 !important; 
            font-weight: 500 !important; 
        }

        /* 4. Brutal Override for Expanders */
        [data-testid="stExpander"] details, 
        [data-testid="stExpander"] summary {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stExpander"] p, 
        [data-testid="stExpander"] span {
            color: #cbd5e1 !important;
        }

        /* 6. Override for Text Inputs */
        div[data-baseweb="input"] > div, 
        div[data-baseweb="input"] input {
            background-color: #0f172a !important;
            color: #00f2fe !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* 7. Normal Buttons */
        [data-testid="stButton"] button {
            background-color: #1e293b !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        [data-testid="stButton"] button:hover {
            border-color: #00f2fe !important;
            color: #00f2fe !important;
            background-color: #0f172a !important;
        }

        /* 8. Fix Invisible Text in Markdown */
        [data-testid="stMarkdownContainer"] p { 
            color: #e2e8f0 !important; 
        }

        /* 9. Footer */
        .premium-footer {
            background: rgba(10, 15, 25, 0.95) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #94a3b8 !important;
        }
        .premium-footer a { 
            color: #38bdf8 !important; 
        }
        .premium-footer a:hover {
            color: #e0f2fe !important;
            text-shadow: 0px 0px 10px rgba(56, 189, 248, 0.8) !important;
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

def render_custom_responsive_css():
    """
    Renders additional custom CSS for main titles and search results UI.
    """
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