import streamlit as st
import pandas as pd
import os
import sys
import logging
from typing import List, Optional

# Ensure the root directory is in the python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from phase2.input_validator import InputValidator
from phase2.models import UserInput
from phase4.recommender import LLMRecommender

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Zomato AI - Best Eats in Bangalore",
    page_icon="🍴",
    layout="centered"
)

# Custom CSS for Glassmorphism
GLASS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    :root {
        --primary: #FF385C;
        --primary-dark: #D70466;
        --bg-dark: #0a0c10;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-white: #ffffff;
        --text-dim: #9ca3af;
        --accent-blue: #3b82f6;
        --accent-purple: #a855f7;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Outfit', sans-serif;
    }

    /* Background Blobs */
    .background-blobs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        filter: blur(80px);
    }

    .blob {
        position: absolute;
        border-radius: 50%;
        opacity: 0.4;
        animation: move 20s infinite alternate;
    }

    .blob-1 {
        width: 400px;
        height: 400px;
        background: var(--primary);
        top: -100px;
        right: -100px;
    }

    .blob-2 {
        width: 350px;
        height: 350px;
        background: var(--accent-blue);
        bottom: -50px;
        left: -50px;
        animation-delay: -5s;
    }

    .blob-3 {
        width: 300px;
        height: 300px;
        background: var(--accent-purple);
        top: 40%;
        left: 30%;
        animation-delay: -10s;
    }

    @keyframes move {
        from { transform: translate(0, 0) scale(1); }
        to { transform: translate(50px, 50px) scale(1.1); }
    }

    /* Main Container Styles */
    .main-header {
        text-align: center;
        margin-bottom: 50px;
        padding-top: 40px;
    }

    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        color: white !important;
    }

    .highlight {
        color: var(--primary);
    }

    .tagline {
        color: var(--text-dim);
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    .stats-bar {
        display: inline-flex;
        align-items: center;
        gap: 15px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.9rem;
        color: var(--text-dim);
    }

    .stat-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .stat-item span {
        color: var(--primary);
        font-weight: 600;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 30px;
    }

    /* Restaurant Card specific Styles */
    .restaurant-card {
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .res-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    .res-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: white;
    }

    .res-rating {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 600;
    }

    .res-meta {
        color: var(--text-dim);
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    .res-meta p {
        margin-bottom: 5px;
    }

    .res-reasoning {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid var(--primary);
        padding: 15px;
        border-radius: 0 12px 12px 0;
        font-size: 0.95rem;
        color: #e5e7eb;
        font-style: italic;
    }

    /* Streamlit Input Overrides */
    .stSelectbox, .stMultiSelect, .stNumberInput {
        background: transparent !important;
    }
    
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(255, 56, 92, 0.3) !important;
    }

    .powered-by {
        text-align: center;
        margin: 40px 0 20px;
        font-size: 0.85rem;
        color: var(--text-dim);
        opacity: 0.6;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
</style>
"""

# HTML for background blobs
BLOBS_HTML = """
<div class="background-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
</div>
"""

def main():
    # Inject CSS and Background
    st.markdown(GLASS_CSS, unsafe_allow_html=True)
    st.markdown(BLOBS_HTML, unsafe_allow_html=True)

    # Load Data and Models
    validator = InputValidator()
    # Cache valid localities and cuisines
    if 'localities' not in st.session_state:
        st.session_state.localities = validator.get_valid_localities()
    if 'cuisines_list' not in st.session_state:
        # Filter out 'Cafe' and 'Unknown'
        raw_cuisines = validator.get_valid_cuisines()
        st.session_state.cuisines_list = [c for c in raw_cuisines if c not in ['Cafe', 'Unknown']]

    recommender = LLMRecommender()

    # Header Section
    st.markdown(f"""
    <div class="main-header">
        <h1>Zomato AI <span class="highlight">Recommender</span></h1>
        <p class="tagline">Helping you find the best places to eat in <span class="highlight">Bangalore</span> city</p>
        <div class="stats-bar">
            <span class="stat-item">📍 <span>{len(st.session_state.localities)}</span> Localities</span>
            <span class="stat-separator">|</span>
            <span class="stat-item">🍴 <span>{len(st.session_state.cuisines_list)}</span> Cuisines</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search Form Section
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            city = st.selectbox(
                "Select locality *",
                options=[""] + st.session_state.localities,
                format_func=lambda x: "Select locality..." if x == "" else x,
                index=0
            )
            
            price_range = st.selectbox(
                "Price Range *",
                options=["", "budget", "mid-range", "premium"],
                format_func=lambda x: {
                    "": "Select price range...",
                    "budget": "Budget (₹ < 500)",
                    "mid-range": "Mid-range (₹500 - ₹1500)",
                    "premium": "Premium (₹ > 1500)"
                }.get(x),
                index=0
            )

        with col2:
            cuisines = st.multiselect(
                "Cuisines (Optional)",
                options=st.session_state.cuisines_list,
                placeholder="Select cuisines..."
            )
            
            min_rating = st.number_input(
                "Min Rating",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=0.1,
                format="%.1f"
            )

        # Submit button
        submit_clicked = st.button("Get Recommendations ✨")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Results Section
    if submit_clicked:
        if not city:
            st.error("Locality is required! Please select a locality to continue.")
        elif not price_range:
            st.error("Price Range is required! Please select a price range to continue.")
        else:
            with st.spinner("Asking the AI for the best spots..."):
                try:
                    # Prepare input
                    user_input = UserInput(
                        city=city,
                        price_range=price_range,
                        cuisine=cuisines if cuisines else None,
                        min_rating=min_rating
                    )
                    
                    # Fetch recommendations from Phase 3 (engine)
                    engine_response = recommender.engine.get_recommendations(user_input, limit=5)
                    
                    if engine_response.count == 0:
                        st.info(f"I'm sorry, but I couldn't find any restaurants in {city} matching your criteria.")
                    else:
                        # Get AI Reasoning Summary (new feature from Phase 6 logic)
                        from phase6.api_server import generate_ai_summary
                        ai_summary = generate_ai_summary(user_input, engine_response.recommendations)
                        
                        # Display Summary
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 4px solid var(--accent-purple);">
                            <p style="color: #e5e7eb; font-style: italic; font-size: 1.1rem;">{ai_summary}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display Cards in columns
                        cols = st.columns(2)
                        for i, rec in enumerate(engine_response.recommendations):
                            # Generate reasoning if not present (Phase 3 recs don't have reasoning, but LLMRecommender can add it)
                            reasoning = recommender.get_individual_reasoning(user_input, rec)
                            clean_reasoning = reasoning.replace("Why you'll like it:", "<strong>Why you'll like it:</strong>")
                            
                            with cols[i % 2]:
                                st.markdown(f"""
                                <div class="glass-card restaurant-card">
                                    <div class="res-header">
                                        <div class="res-name">{rec.name}</div>
                                        <span class="res-rating">{rec.rating} ★</span>
                                    </div>
                                    <div class="res-meta">
                                        <p>🍴 {rec.cuisines}</p>
                                        <p>💰 Avg. ₹{rec.average_cost} for two</p>
                                        <p>📍 {rec.address}</p>
                                    </div>
                                    <div class="res-reasoning">
                                        {clean_reasoning}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
                    logger.error(f"Error in streamlit_app: {e}", exc_info=True)

    # Footer
    st.markdown("""
    <footer class="powered-by">
        Powered By Groq AI
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
