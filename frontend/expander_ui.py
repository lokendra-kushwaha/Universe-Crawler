import streamlit as st

def render_expander_css_ui():
    """Renders the custom CSS, Glowing Box, Title, and Quote for the VIP Expander."""
    st.markdown("""
        <style>
        /* ======================================================== */
        /* CRAWLER SECTION TITLE & QUOTE STYLES                     */
        /* ======================================================== */
        
        /* Light Mode (Default) */
        .custom-crawler-title {
            font-size: 1.5rem;
            font-weight: 800;
            text-align: center;
            color: #222222;
            line-height: 1.2;
            transition: color 0.3s ease;
        }
        
        .custom-crawler-quote {
            font-size: 0.9rem;
            color: #666666;
            text-align: center;
            font-style: italic;
            margin-top: 5px;
            margin-bottom: 25px;
            transition: color 0.3s ease;
        }

        /* Auto Dark Mode Overrides */
        @media (prefers-color-scheme: dark) {
            .custom-crawler-title {
                color: #00f2fe !important; /* Premium Neon Blue */
                text-shadow: 0px 2px 10px rgba(0, 242, 254, 0.4) !important;
            }
            .custom-crawler-quote {
                color: #94a3b8 !important; /* Soft Slate Grey for clear visibility */
            }
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
            
        /* ======================================================== */
        /* EXPANDER UI STYLES (LIGHT MODE DEFAULTS)                 */
        /* ======================================================== */

        /* 1. Main Box: Glowing Blue Border & Soft Shadow */
        div[data-testid="stExpander"] {
            border: 1.5px solid #1a73e8 !important; /* Blue */
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


        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {
            
            /* 1. Main Box Dark Mode */
            div[data-testid="stExpander"] {
                background: linear-gradient(145deg, #0f172a, #1e293b) !important; /* Dark Navy Glass */
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
            }

            /* 2. Hover Effect Dark Mode */
            div[data-testid="stExpander"]:hover {
                border: 1px solid rgba(0, 242, 254, 0.4) !important; /* Neon Blue Border Glow */
                box-shadow: 0 6px 25px rgba(0, 242, 254, 0.15) !important; /* Neon Shadow */
            }

            /* 3. Expander Header Dark Mode */
            div[data-testid="stExpander"] summary {
                background-color: rgba(30, 41, 59, 0.8) !important; /* Darker Glass Header */
            }

            /* 4. Text inside the Expander Header Dark Mode */
            div[data-testid="stExpander"] summary p {
                color: #00f2fe !important; /* Glowing Neon Blue Text */
            }
            
            /* 5. The line icon (chevron) color Dark Mode */
            div[data-testid="stExpander"] summary svg {
                fill: #00f2fe !important;
                color: #00f2fe !important;
            }
        }
        </style>
        
        <div class="custom-crawler-title">🕷️ Crawl The Universe</div>
        <div class="custom-crawler-quote">"Define your search universe"</div>
    """, unsafe_allow_html=True)

def render_expander_seed_label_ui():
    """Renders the HTML for the Seed URL input label."""
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