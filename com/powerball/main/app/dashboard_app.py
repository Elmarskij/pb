import streamlit as st
from datetime import datetime
from com.powerball.main.utility.common_utilities import CommonUtilities

# Import the section renderers
from com.powerball.main.app.charts.frequency_bar import render_main_section
from com.powerball.main.app.charts.individual_frequency_bar import render_individual_section


def run_dashboard(input_data):
    st.set_page_config(page_title="Lottery Dashboard", layout="wide")

    # CSS for max width behavior
    st.markdown("""
        <style>
        .block-container {
            max_width: 2400px; 
            padding-left: 2rem; 
            padding-right: 2rem; 
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("📊 Lottery Frequency Dashboard")

    # 1. LOAD CONFIG
    try:
        min_date = datetime.strptime(CommonUtilities.get_from_config("min_date"), "%m-%d-%Y").date()
        max_date = datetime.strptime(CommonUtilities.get_from_config("max_date"), "%m-%d-%Y").date()
    except Exception as e:
        st.error(f"Error reading config: {e}")
        st.stop()

    # 2. SIDEBAR (Global Settings)
    st.sidebar.header("⚙️ Settings")
    global_override = st.sidebar.checkbox("Override All Date Filters", value=True)

    global_start, global_end = min_date, max_date
    if global_override:
        st.sidebar.write("Global range active:")
        global_start, global_end = st.sidebar.slider(
            "Select Global Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )

    # Pack global state into a tuple to pass down to utility functions
    global_state = (global_override, global_start, global_end)

    # 3. RENDER SECTIONS

    # A. Render Main & Powerball Section
    render_main_section(input_data, min_date, max_date, global_state)

    st.markdown("---")

    # B. Render Individual Numbers Section
    render_individual_section(input_data, min_date, max_date, global_state)
