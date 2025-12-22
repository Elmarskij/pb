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

    if input_data.empty:
        st.error("No data available to display.")
        st.stop()

    # 1. DETERMINE DATA BOUNDS (Absolute limits based on actual fetched data)
    # These determine the MIN/MAX of the slider itself.
    data_min_date = input_data['Date'].min().date()
    data_max_date = input_data['Date'].max().date()

    # 2. LOAD CONFIG DEFAULTS
    # These determine the DEFAULT SELECTION handles on the slider.
    try:
        config_min_str = CommonUtilities.get_from_config("min_date")
        config_max_str = CommonUtilities.get_from_config("max_date")

        config_min = datetime.strptime(config_min_str, "%m-%d-%Y").date()
        config_max = datetime.strptime(config_max_str, "%m-%d-%Y").date()
    except Exception as e:
        st.warning(f"Could not read config dates: {e}. Defaulting to full data range.")
        config_min, config_max = data_min_date, data_max_date

    # 3. SIDEBAR (Global Settings)
    st.sidebar.header("⚙️ Settings")
    global_override = st.sidebar.checkbox("Override All Date Filters", value=True)

    # Logic: Default to Config, but clamp to Data Range.
    # If Config Max is in the future (e.g., 2026), it clamps to Data Max (Today/Latest Draw).
    default_start = max(data_min_date, config_min)
    default_end = min(data_max_date, config_max)

    # Safety: If clamping caused start > end, reset to full range
    if default_start > default_end:
        default_start, default_end = data_min_date, data_max_date

    global_start, global_end = default_start, default_end

    if global_override:
        st.sidebar.write("Global range active:")
        # Slider allows full range (data_min/max) but starts at default_start/end
        global_start, global_end = st.sidebar.slider(
            "Select Global Range",
            min_value=data_min_date,
            max_value=data_max_date,
            value=(default_start, default_end)
        )

    # Pack global state
    global_state = (global_override, global_start, global_end)

    # 4. RENDER SECTIONS
    # A. Render Main & Powerball Section
    render_main_section(input_data, data_min_date, data_max_date, global_state)

    st.markdown("---")

    # B. Render Individual Numbers Section
    render_individual_section(input_data, data_min_date, data_max_date, global_state)
