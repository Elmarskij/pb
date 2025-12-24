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

    # 1. SETUP DATE RANGE (Min/Max from Data)
    min_date_data = input_df['Date'].min().date()
    max_date_data = input_df['Date'].max().date()

    # 2. LOAD CONFIG DEFAULTS
    try:
        cfg_min_str = CommonUtilities.get_from_config("min_date")
        cfg_min_dt = datetime.strptime(cfg_min_str, "%m-%d-%Y").date()
    except Exception:
        cfg_min_dt = min_date_data

    # Ensure config start is within actual data bounds
    default_start = max(min_date_data, cfg_min_dt)
    if default_start > max_date_data:
        default_start = min_date_data

    # 3. SIDEBAR SLIDER (Global Filter)
    st.sidebar.header("⚙️ Settings")
    st.sidebar.write("### Filter Data Range")

    # This slider returns actual Python Date objects
    start_date, end_date = st.sidebar.slider(
        "Select Date Range",
        min_value=min_date_data,
        max_value=max_date_data,
        value=(default_start, max_date_data),
        format="MM/DD/YYYY"
    )

    # 4. FILTER DATA (Server-Side)
    # We filter the dataframe HERE. This ensures the charts receive only valid data.
    # This solves the "Infinite extent" error completely.
    mask = (input_df['Date'].dt.date >= start_date) & (input_df['Date'].dt.date <= end_date)
    filtered_df = input_df.loc[mask]

    st.info(f"Showing results from **{start_date}** to **{end_date}** ({len(filtered_df)} draws)")

    # 5. BUILD SECTIONS (Using Filtered Data)
    # We don't pass a slider param anymore, just the data.
    gen_main = FrequencyChartGenerator(filtered_df)
    chart_main = gen_main.build_section()

    gen_ind = IndividualFrequencyChartGenerator(filtered_df)
    chart_ind = gen_ind.build_section()

    # 6. COMBINE & RENDER
    final_dashboard = alt.vconcat(
        chart_main,
        chart_ind
    ).resolve_scale(
        color='independent'
    ).configure_view(
        stroke=None
    )

    st.altair_chart(final_dashboard, use_container_width=True)
