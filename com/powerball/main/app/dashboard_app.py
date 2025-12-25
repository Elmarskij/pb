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

    if 'ts_days' not in input_df.columns:
        st.error("❌ ERROR: ts_days column missing. Clear cache and reload.")
        st.cache_data.clear()
        return

    # 1. CALCULATE BOUNDS (Integer Days)
    min_days = int(input_df['ts_days'].min())
    max_days = int(input_df['ts_days'].max())

    # 2. CONFIG DEFAULT
    try:
        cfg_min_str = CommonUtilities.get_from_config("min_date")
        cfg_min_dt = datetime.strptime(cfg_min_str, "%m-%d-%Y")
        start_days_config = (cfg_min_dt - datetime(1970, 1, 1)).days
    except Exception:
        start_days_config = min_days

    default_start = max(min_days, start_days_config)
    if default_start > max_days:
        default_start = min_days

    st.sidebar.info("ℹ️ Charts now update **instantly** as you drag the slider below the charts.")

    # 3. CREATE ALTAIR PARAM (Client-Side Slider)
    # This slider lives inside the chart logic, not Streamlit.
    slider = alt.binding_range(
        min=min_days,
        max=max_days,
        step=1,
        name='Start Day (Epoch): '
    )

    date_param = alt.param(
        name='date_filter',
        value=default_start,
        bind=slider
    )

    # 4. BUILD SECTIONS (Pass the Param, not filtered data)
    # We pass the FULL dataset. Filtering happens in the browser.

    # --- Section 1: Main (65%) & Powerball (35%) ---
    gen_main = FrequencyChartGenerator(input_df)
    chart_main, chart_pb = gen_main.build_section(date_param)

    col1, col2 = st.columns([0.65, 0.35], gap="large")

    with col1:
        st.altair_chart(chart_main, width="stretch")
    with col2:
        st.altair_chart(chart_pb, width="stretch")

    st.markdown('<hr style="height:3px;border:none;color:#999;background-color:#999;" />', unsafe_allow_html=True)

    # --- Section 2: Individual Positions (Grid) ---
    gen_ind = IndividualFrequencyChartGenerator(input_df)
    chart_list = gen_ind.build_section(date_param)

    for i in range(0, 6, 2):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.altair_chart(chart_list[i], width="stretch")
        with c2:
            if i + 1 < len(chart_list):
                st.altair_chart(chart_list[i + 1], width="stretch")
        st.markdown("---")
