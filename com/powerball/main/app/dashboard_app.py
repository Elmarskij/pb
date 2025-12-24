import streamlit as st
import logging
import altair as alt
import pandas as pd
from datetime import datetime, date
from com.powerball.main.utility.common_utilities import CommonUtilities
from com.powerball.main.app.service.lotto_data_service import LottoDataService
from com.powerball.main.app.charts.frequency_bar import FrequencyChartGenerator
from com.powerball.main.app.charts.individual_frequency_bar import IndividualFrequencyChartGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def run_dashboard(input_df):
    st.set_page_config(page_title="Lottery Dashboard", layout="wide")
    st.markdown("""<style>.block-container {max_width: 2400px; padding: 2rem;}</style>""", unsafe_allow_html=True)
    st.title("📊 Real-Time Lottery Dashboard")

    if input_df.empty:
        st.error("❌ ERROR: Input DataFrame is EMPTY.")
        return

    # 1. SETUP DATE RANGE
    min_date_data = input_df['Date'].min().date()
    max_date_data = input_df['Date'].max().date()

    # 2. LOAD CONFIG DEFAULTS
    try:
        cfg_min_str = CommonUtilities.get_from_config("min_date")
        cfg_min_dt = datetime.strptime(cfg_min_str, "%m-%d-%Y").date()
    except Exception:
        cfg_min_dt = min_date_data

    default_start = max(min_date_data, cfg_min_dt)
    if default_start > max_date_data:
        default_start = min_date_data

    # 3. SIDEBAR SLIDER (Global Filter)
    st.sidebar.header("⚙️ Settings")
    st.sidebar.write("### Filter Data Range")

    start_date, end_date = st.sidebar.slider(
        "Select Date Range",
        min_value=min_date_data,
        max_value=max_date_data,
        value=(default_start, max_date_data),
        format="MM/DD/YYYY"
    )

    # 4. FILTER DATA (Server-Side)
    mask = (input_df['Date'].dt.date >= start_date) & (input_df['Date'].dt.date <= end_date)
    filtered_df = input_df.loc[mask]

    if filtered_df.empty:
        st.warning("No draws found in this date range.")
        return

    # 5. BUILD SECTIONS
    # --- Section 1: Main (65%) & Powerball (35%) ---
    gen_main = FrequencyChartGenerator(filtered_df)
    chart_main, chart_pb = gen_main.build_section()

    col1, col2 = st.columns([0.65, 0.35], gap="large")

    with col1:
        st.altair_chart(chart_main, use_container_width=True)
    with col2:
        st.altair_chart(chart_pb, use_container_width=True)

    st.markdown('<hr style="height:3px;border:none;color:#999;background-color:#999;" />', unsafe_allow_html=True)

    # --- Section 2: Individual Positions (Grid) ---
    gen_ind = IndividualFrequencyChartGenerator(filtered_df)
    chart_list = gen_ind.build_section()

    # Create 3 rows of 2 columns
    for i in range(0, 6, 2):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.altair_chart(chart_list[i], use_container_width=True)
        with c2:
            if i + 1 < len(chart_list):
                st.altair_chart(chart_list[i + 1], use_container_width=True)
        st.markdown("---")
