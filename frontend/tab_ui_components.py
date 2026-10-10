import streamlit as st
import streamlit.components.v1 as components


def render_search_header_ui():
    """Renders the main search title"""
    st.markdown('<h4 class="responsive-search-title">🔍 Search Your Indexed Universe</h4>', unsafe_allow_html=True)

def render_search_mode_toggle_ui():
    st.markdown("""
    <style>
    /* ======================================================== */
    /* STYLE SEGMENTED CONTROLS (RADIO PILLS) - LIGHT MODE      */
    /* ======================================================== */

    /* 1. Main container background (Light Gray Pill) */
    div[role="radiogroup"] {
        background-color: #f1f3f4 !important;
        padding: 4px !important;
        border-radius: 30px !important;
        display: inline-flex !important;
        gap: 0 !important;
        border: 1px solid #e8eaed !important;
        width: fit-content !important;
        transition: all 0.3s ease !important;
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
        color: #1a73e8 !important; 
    }
    
    /* 6. Active state text styling */
    div[role="radiogroup"] label:has(input:checked) div {
        font-weight: 700 !important;
    }

    /* ======================================================== */
    /* MOBILE FIX                                               */
    /* ======================================================== */
    @media screen and (max-width: 636px) {
        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important; /* Force Side-by-Side */
            width: 100% !important;
        }

        div[role="radiogroup"] label {
            flex: 1 !important;
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

    /* ======================================================== */
    /* AUTO DARK MODE OVERRIDES                                 */
    /* ======================================================== */
    @media (prefers-color-scheme: dark) {
        div[role="radiogroup"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2) !important;
        }
        div[role="radiogroup"] label {
            color: #94a3b8 !important; 
        }
        div[role="radiogroup"] label:hover {
            color: #cbd5e1 !important; 
        }
        div[role="radiogroup"] label:has(input:checked) {
            background-color: rgba(30, 41, 59, 0.95) !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.15) !important; 
            color: #00f2fe !important; 
        }
        div[role="radiogroup"] label:has(input:checked) div {
            text-shadow: 0px 0px 8px rgba(0, 242, 254, 0.4) !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_trending_searches_ui():
    """Renders the HTML grid for trending searches"""
    trending_html = """
    <style>    
        /* ======================================================== */
        /* TRENDING SEARCHES CHIPS (LIGHT MODE & LAYOUT)            */
        /* ======================================================== */
        
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
            transition: all 0.3s ease-in-out;
        }
        
        /* Hover effect */
        .custom-chip:hover {
            background-color: #f8f9fa;
            border-color: #dadce0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            color: #202124;
            transform: translateY(-1.5px); /* Smooth floating effect */
        }

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {
            
            .custom-chip {
                background-color: rgba(30, 41, 59, 0.6) !important; /* Dark Slate Glass */
                border: 1px solid rgba(255, 255, 255, 0.1) !important; /* Subtle border */
                color: #cbd5e1 !important; /* Soft light grey text */
                box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
            }
            
            .custom-chip:hover {
                background-color: rgba(15, 23, 42, 0.9) !important; /* Deeper dark on hover */
                border-color: rgba(0, 242, 254, 0.4) !important; /* Neon Blue Border */
                color: #00f2fe !important; /* Glowing Neon Cyan Text */
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important; /* Neon Glow */
                transform: translateY(-2px); /* Enhanced float in dark mode */
            }
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
    st.markdown(trending_html, unsafe_allow_html=True)

def render_fuzzy_suggestion_ui(search_word, suggestion):
    """Renders the Did you mean / Fuzzy suggestion box"""
    st.markdown(f"""
        <style>
        /* ======================================================== */
        /* SPELL CHECKER ALERT (LIGHT MODE DEFAULTS)                */
        /* ======================================================== */
        .spell-check-alert {{
            background-color: #fce8e6; 
            color: #d93025; 
            padding: 12px 15px; 
            border-radius: 8px; 
            margin-bottom: 20px; 
            font-size: 1.05rem;
            transition: all 0.3s ease;
        }}
        .spell-check-suggestion {{
            color: #1a73e8; 
            cursor: pointer; 
            text-decoration: underline;
            font-weight: 600;
            transition: color 0.3s ease;
        }}

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {{
            .spell-check-alert {{
                background-color: rgba(255, 59, 48, 0.1) !important; /* Dark glass red */
                border: 1px solid rgba(255, 59, 48, 0.3) !important;
                color: #e2e8f0 !important; /* Soft white/grey text for readability */
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            }}
            .spell-check-alert b {{
                color: #ff4d4d !important; /* Glowing neon red for emphasis */
                text-shadow: 0px 0px 5px rgba(255, 77, 77, 0.3) !important;
            }}
            .spell-check-suggestion {{
                color: #00f2fe !important; /* Neon Cyan for the clickable suggestion */
                text-shadow: 0px 0px 8px rgba(0, 242, 254, 0.4) !important;
            }}
            .spell-check-suggestion:hover {{
                color: #e0f2fe !important; /* Brighter on hover */
                text-shadow: 0px 0px 12px rgba(0, 242, 254, 0.6) !important;
            }}
        }}
        </style>

        <div class="spell-check-alert">
            ❌ No exact match for '<b>{search_word}</b>'. <br>
            💡 <b>Did you mean:</b> <span class="spell-check-suggestion">{suggestion}</span> ?
        </div>
    """, unsafe_allow_html=True)

def render_search_stats_banner_ui(num_results, total_search_time, engine_badge):
    """Renders the premium results count and time banner"""
    st.markdown(f"""
        <style>
        /* ======================================================== */
        /* SEARCH STATS BAR (LIGHT MODE DEFAULTS)                   */
        /* ======================================================== */
        .search-stats-container {{
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); 
            border-left: 4px solid #1a73e8; 
            padding: 12px 20px; 
            border-radius: 4px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            transition: all 0.3s ease;
        }}
        .search-stats-text {{
            color: #202124; 
            font-size: 0.95rem; 
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        .search-stats-badge {{
            background-color: #1a73e8; 
            color: white; 
            padding: 4px 10px; 
            border-radius: 12px; 
            font-size: 0.75rem; 
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {{
            .search-stats-container {{
                background: rgba(30, 41, 59, 0.6) !important; /* Dark Glass */
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-left: 4px solid #00f2fe !important; /* Neon Cyan Border */
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            }}
            .search-stats-text {{
                color: #e2e8f0 !important; /* Soft white for readability */
            }}
            .search-stats-text b {{
                color: #00f2fe !important; /* Highlight variables in neon */
                text-shadow: 0 0 5px rgba(0, 242, 254, 0.3) !important;
            }}
            .search-stats-badge {{
                background-color: rgba(0, 242, 254, 0.15) !important; /* Translucent Neon Glass */
                color: #00f2fe !important; /* Neon text */
                border: 1px solid rgba(0, 242, 254, 0.5) !important;
                box-shadow: 0 0 10px rgba(0, 242, 254, 0.4) !important; /* Glowing effect */
            }}
        }}
        </style>

        <div class="search-stats-container">
            <span class="search-stats-text">
                Found <b>{num_results}</b> results in <b>{total_search_time:.4f}s</b>
            </span>
            <span class="search-stats-badge">
                {engine_badge}
            </span>
        </div>
    """, unsafe_allow_html=True)

def render_premium_export_divider():
    """
    Renders a premium gradient divider and styles the Streamlit native download button.
    Includes both Light Mode defaults and Cyber-Glassmorphism Dark Mode overrides.
    """
    st.markdown("""
        <style>
        /* ======================================================== */
        /* EXPORT BUTTON & DIVIDER (LIGHT MODE DEFAULTS)            */
        /* ======================================================== */
        
        /* 1. Target Streamlit's Native Download Button */
        [data-testid="stDownloadButton"] button {
            background-color: #ffffff !important;
            border: 1px solid #dfe1e5 !important;
            color: #1a73e8 !important; /* Premium Google Blue */
            border-radius: 20px !important;
            padding: 4px 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        }
        
        [data-testid="stDownloadButton"] button:hover {
            border-color: #1a73e8 !important;
            background-color: #f8f9fa !important;
            box-shadow: 0 4px 10px rgba(26, 115, 232, 0.15) !important;
            transform: translateY(-2px) !important;
        }

        /* 2. Premium Gradient Divider Line */
        .premium-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #dfe1e5, transparent);
            margin-top: 15px;
            margin-bottom: 25px;
            border: none;
        }

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {
            
            [data-testid="stDownloadButton"] button {
                background-color: rgba(30, 41, 59, 0.6) !important; /* Dark Glass */
                border: 1px solid rgba(0, 242, 254, 0.3) !important; /* Neon Border */
                color: #00f2fe !important; /* Neon Cyan Text */
                box-shadow: 0 2px 8px rgba(0, 242, 254, 0.1) !important;
            }
            
            [data-testid="stDownloadButton"] button:hover {
                background-color: rgba(15, 23, 42, 0.9) !important;
                border-color: #00f2fe !important;
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important; /* Neon Glow */
                color: #ffffff !important; /* Bright white text on hover */
                text-shadow: 0 0 5px rgba(0, 242, 254, 0.8) !important;
            }

            .premium-divider {
                background: linear-gradient(90deg, transparent, rgba(0, 242, 254, 0.3), transparent);
            }
        }
        </style>
        
        <hr class="premium-divider">
    """, unsafe_allow_html=True)

def render_individual_result_ui(url, display_url, actual_rank, display_title, final_snippet, score, is_ai_mode):
    """Renders a single search result with Google-style formatting"""
    score_label = '🎯 Final Fused Score:' if is_ai_mode else '📈 PageRank Score:'
    
    st.markdown(f"""
    <style>
        /* ======================================================== */
        /* SEARCH RESULTS STYLING (LIGHT MODE DEFAULTS)             */
        /* ======================================================== */
        .result-container {{
            margin-bottom: 25px; 
            padding-bottom: 15px; 
            border-bottom: 1px solid #f1f3f4;
            transition: all 0.3s ease;
        }}
        .result-url {{
            color: #202124; 
            font-size: 0.85rem; 
            margin-bottom: 4px; 
            text-decoration: none; 
            display: block; 
            opacity: 0.7;
            transition: color 0.3s ease;
        }}
        .result-url:hover {{
            opacity: 1;
        }}
        .result-title-wrapper {{
            font-size: 1.25rem; 
            font-weight: 400; 
            margin-bottom: 6px; 
            font-family: 'Google Sans', Arial, sans-serif;
        }}
        .result-title-link {{
            color: #1a0dab; 
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        .result-title-link:hover {{
            text-decoration: underline;
        }}
        .result-snippet {{
            font-size: 0.95rem; 
            color: #4d5156; 
            line-height: 1.5; 
            margin-bottom: 6px;
            transition: color 0.3s ease;
        }}
        .result-score {{
            font-size: 0.8rem; 
            color: #1a73e8; 
            font-weight: 500;
            transition: color 0.3s ease;
        }}

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {{
            .result-container {{
                border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            }}
            .result-url {{
                color: #94a3b8 !important; /* Soft slate grey */
            }}
            .result-title-link {{
                color: #38bdf8 !important; /* Bright Cyber Blue */
            }}
            .result-title-link:hover {{
                color: #00f2fe !important; /* Neon Cyan on hover */
                text-shadow: 0 0 8px rgba(0, 242, 254, 0.4) !important;
            }}
            
            .result-snippet {{
            color: #cbd5e1 !important; /* Light silver for reading clarity */
            line-height: 1.2 !important;
            }}
        
            /* HIGHLIGHTED SEARCH KEYWORDS IN SNIPPET */
            .result-snippet b, .result-snippet strong {{
                color: #00f2fe !important; /* Neon Cyan for exactly matched keywords */
                text-shadow: 0 0 8px rgba(0, 242, 254, 0.5) !important;
            }}

            .result-score {{
                color: #00f2fe !important; /* Glowing Neon Cyan */
                text-shadow: 0px 0px 5px rgba(0, 242, 254, 0.3) !important;
            }}
        }}
    </style>

    <div class="result-container">
        <a href="{url}" target="_blank" class="result-url">
            {display_url}
        </a>
        <div class="result-title-wrapper">
            <a href="{url}" target="_blank" class="result-title-link">
                {actual_rank}. {display_title}
            </a>
        </div>
        <div class="result-snippet">
            {final_snippet}
        </div>
        <div class="result-score">
            {score_label} {score:.6f}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_crawler_header_ui():
    """Renders the Title and Quote for the Crawler Tab with custom responsive CSS."""
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
        </style>
        
        <div class="custom-crawler-title">🕷️ Crawl The Universe</div>
        <div class="custom-crawler-quote">"Define your search universe"</div>
    """, unsafe_allow_html=True)

def render_seed_url_label_ui():
    """Renders the HTML label for the Seed URL input box."""
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

def render_insight_metrics_ui(total_pages, total_words, max_pr_score, avg_links):
    """Renders the 4 premium metric cards for the Insights Dashboard"""
    st.markdown(f"""
    <style>
    /* ======================================================== */
    /* ANALYTICS DASHBOARD METRIC CARDS (LIGHT MODE)            */
    /* ======================================================== */
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
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
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
        transition: color 0.3s ease;
    }}
    .metric-label {{
        font-size: 0.8rem;
        color: #5f6368;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: color 0.3s ease;
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

    /* ======================================================== */
    /* AUTO DARK MODE OVERRIDES                                 */
    /* ======================================================== */
    @media (prefers-color-scheme: dark) {{
        
        .metric-card {{
            background: rgba(30, 41, 59, 0.6) !important; /* Dark Slate Glass */
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }}
        
        .metric-card:hover {{
            background: rgba(15, 23, 42, 0.9) !important; /* Deep Navy on Hover */
            border-color: rgba(0, 242, 254, 0.4) !important; /* Neon Cyan Border */
            box-shadow: 0 8px 25px rgba(0, 242, 254, 0.15) !important; /* Neon Glow Shadow */
            transform: translateY(-5px);
        }}

        .metric-value {{
            color: #00f2fe !important; /* Glowing Neon Cyan Numbers */
            text-shadow: 0px 0px 10px rgba(0, 242, 254, 0.3) !important;
        }}

        .metric-label {{
            color: #94a3b8 !important; /* Soft Slate Grey for readability */
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

def render_print_button_ui():
    """Renders the custom JS print button"""
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

def render_admin_system_analytics_header():
    """
    Renders the premium 'System Analytics' header for the Admin Dashboard.
    Includes both Light Mode defaults and Cyber-Glassmorphism Dark Mode overrides.
    """
    st.markdown("""
        <style>
        /* ======================================================== */
        /* ADMIN SECTION HEADER (LIGHT MODE DEFAULTS)               */
        /* ======================================================== */
        .admin-header-container {
            margin-top: 10px;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f1f3f4;
            transition: all 0.3s ease;
        }
        
        .admin-header-title {
            color: #202124;
            font-family: 'Google Sans', Arial, sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: color 0.3s ease;
        }
        
        .admin-header-icon {
            background: #fce8e6;
            color: #d93025;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 1.2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }

        /* ======================================================== */
        /* AUTO DARK MODE OVERRIDES                                 */
        /* ======================================================== */
        @media (prefers-color-scheme: dark) {
            .admin-header-container {
                border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            .admin-header-title {
                color: #f8fafc !important; /* Bright white text for visibility */
            }
            
            .admin-header-icon {
                background: rgba(255, 59, 48, 0.15) !important; /* Translucent dark red glass */
                color: #ff4d4d !important; /* Glowing Neon Red icon */
                box-shadow: 0 0 12px rgba(255, 77, 77, 0.3) !important; /* Neon red glow */
                border: 1px solid rgba(255, 77, 77, 0.4) !important;
            }
        }
        </style>

        <div class="admin-header-container">
            <h3 class="admin-header-title">
                <span class="admin-header-icon">
                    📊
                </span> 
                System Analytics
            </h3>
        </div>
    """, unsafe_allow_html=True)

def render_admin_metrics_ui(total_searches, avg_time, total_indexed):
    """
    Renders the premium UI cards for the Admin Dashboard.
    Keeps the main logic clean by handling all HTML/CSS here.
    """
    st.markdown(f"""
    <style>
    /* ======================================================== */
    /* ADMIN DASHBOARD METRIC CARDS (LIGHT MODE)                */
    /* ======================================================== */
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
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
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
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }}
    .admin-metric-label {{
        font-size: 0.8rem;
        color: #5f6368;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: color 0.3s ease;
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

    /* ======================================================== */
    /* AUTO DARK MODE OVERRIDES                                 */
    /* ======================================================== */
    @media (prefers-color-scheme: dark) {{
        
        .admin-metric-card {{
            background: rgba(30, 41, 59, 0.6) !important; /* Dark Slate Glass */
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        }}
        
        .admin-metric-card:hover {{
            background: rgba(15, 23, 42, 0.9) !important; /* Deep Navy on Hover */
            border-color: rgba(255, 59, 48, 0.5) !important; /* Neon Red Border */
            box-shadow: 0 8px 25px rgba(255, 59, 48, 0.2) !important; /* Red Neon Shadow */
            transform: translateY(-5px);
        }}

        .admin-metric-value {{
            color: #ff4d4d !important; /* Glowing Neon Red Numbers */
            text-shadow: 0px 0px 10px rgba(255, 77, 77, 0.4) !important;
        }}

        .admin-metric-label {{
            color: #94a3b8 !important; /* Soft Slate Grey */
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
