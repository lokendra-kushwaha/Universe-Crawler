import streamlit as st
import time

def render_custom_loader():
    """
    Renders a premium Cyber-Glassmorphism loading screen.
    Returns a Streamlit placeholder object so it can be cleared after loading.
    """
    loader_placeholder = st.empty()
    
    with loader_placeholder.container():
        st.markdown("""
            <style>
            /* ======================================================== */
            /* PREMIUM CYBER-LOADER STYLES                              */
            /* ======================================================== */
            .custom-loader-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 60vh;
                font-family: 'Courier New', Courier, monospace;
            }
            
            /* ======================================================== */
            /* PREMIUM LOADER (LIGHT MODE DEFAULTS)                     */
            /* ======================================================== */
            .neon-spinner {
                width: 60px;
                height: 60px;
                border: 4px solid rgba(26, 115, 232, 0.1);
                border-radius: 50%;
                border-top-color: #1a73e8; /* Premium Google Blue */
                border-bottom-color: #1a73e8;
                animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
                margin-bottom: 25px;
                box-shadow: 0 0 15px rgba(26, 115, 232, 0.1);
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .loader-text {
                color: #1a73e8; /* Premium Google Blue */
                font-size: 1.2rem;
                font-weight: 700;
                letter-spacing: 4px;
                text-transform: uppercase;
                animation: pulse-text-light 1.5s ease-in-out infinite;
            }
            
            @keyframes pulse-text-light {
                0% { opacity: 0.7; }
                50% { opacity: 1; text-shadow: 0 0 10px rgba(26, 115, 232, 0.3); }
                100% { opacity: 0.7; }
            }

            /* ======================================================== */
            /* AUTO DARK MODE OVERRIDES (CYBER-NEON)                    */
            /* ======================================================== */
            @media (prefers-color-scheme: dark) {
                .neon-spinner {
                    border: 4px solid rgba(0, 242, 254, 0.1) !important;
                    border-top-color: #00f2fe !important;
                    border-bottom-color: #00f2fe !important;
                    box-shadow: 0 0 20px rgba(0, 242, 254, 0.3), inset 0 0 15px rgba(0, 242, 254, 0.2) !important;
                }
                .loader-text {
                    color: #00f2fe !important;
                    text-shadow: 0 0 10px rgba(0, 242, 254, 0.6) !important;
                    animation: pulse-text-dark 1.5s ease-in-out infinite !important;
                }
            }
            
            @keyframes pulse-text-dark {
                0% { opacity: 0.6; }
                50% { opacity: 1; text-shadow: 0 0 20px rgba(0, 242, 254, 0.8); }
                100% { opacity: 0.6; }
            }

            /* ======================================================== */
            /* MOBILE RESPONSIVENESS FOR LOADER TEXT                    */
            /* ======================================================== */
            @media screen and (max-width: 768px) {
                .loader-text {
                    font-size: 0.75rem !important;
                    letter-spacing: 1.5px !important;
                    white-space: nowrap !important;
                }
                .neon-spinner {
                    width: 50px !important;
                    height: 50px !important;
                    margin-bottom: 20px !important;
                }
            }
            </style>

            <div class="custom-loader-container">
                <div class="neon-spinner"></div>
                <div class="loader-text">Initializing Universe Engine...</div>
            </div>
        """, unsafe_allow_html=True)
        
    return loader_placeholder