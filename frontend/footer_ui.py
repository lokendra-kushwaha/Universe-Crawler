import streamlit as st

def render_footer():
    """
    Renders the premium sticky footer across the entire application.
    """
    footer_html = """
    <style>
    /* 1. Add padding to Streamlit's main block so the last content doesn't hide behind the footer */
    .block-container {
        padding-bottom: 100px !important;
    }

    /* ======================================================== */
    /* PREMIUM FOOTER STYLES (LIGHT MODE DEFAULTS)              */
    /* ======================================================== */
    /* 2. Make the footer stick to the bottom */
    .premium-footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        z-index: 9999 !important; /* Keeps footer on top of all other elements */
        background-color: #ffffff !important; /* Solid white background is required */
        text-align: center;
        padding-top: 8px;
        padding-bottom: 10px;
        border-top: 1px solid #e8eaed; 
        box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.05); /* Sleek shadow above the footer */
        color: #5f6368; 
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease; /* Smooth transition for dark mode */
    }
    .premium-footer p {
        margin: 2px 0px !important; 
        line-height: 1.5 !important;
    }
    .premium-footer a {
        color: #1a73e8; 
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .premium-footer a:hover {
        text-decoration: underline;
        color: #1557b0;
    }
    .footer-heart {
        color: #ea4335; 
        font-size: 0.95rem;
    }
    .footer-title {
        font-weight: 700;
        color: #202124;
        transition: color 0.3s ease;
    }

    /* ======================================================== */
    /* AUTO DARK MODE OVERRIDES (CYBER-GLASSMORPHISM FOOTER)    */
    /* ======================================================== */
    @media (prefers-color-scheme: dark) {
        
        .premium-footer {
            background-color: rgba(10, 15, 25, 0.95) !important; /* Dark Glass Background */
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important; /* Subtle light border */
            box-shadow: 0px -4px 15px rgba(0, 0, 0, 0.6) !important; /* Darker shadow */
            color: #94a3b8 !important; /* Soft Slate text */
        }
        
        .premium-footer a {
            color: #38bdf8 !important; /* Neon Blue Links */
        }
        
        .premium-footer a:hover {
            color: #e0f2fe !important; /* Glowing white-blue on hover */
            text-shadow: 0px 0px 10px rgba(56, 189, 248, 0.8) !important;
            text-decoration: none;
        }
        
        .footer-title {
            color: #e2e8f0 !important; /* Brighter white for title in dark mode */
        }
        
        .footer-heart {
            text-shadow: 0px 0px 5px rgba(234, 67, 53, 0.5) !important; /* Soft glow for the heart */
        }
    }
    </style>

    <div class="premium-footer">
        <p>Engineered with <span class="footer-heart">❤️</span> by <span class="footer-title">Lokendra Kushwaha</span></p>
        <p>© 2026 The Universe Crawler Project | <a href="https://github.com/lokendra-kushwaha" target="_blank">GitHub</a> • <a href="https://www.instagram.com/the_lokendra_kushwaha_81" target="_blank">Instagram</a></p>
    </div>
    """

    # Render the sticky footer
    st.markdown(footer_html, unsafe_allow_html=True)