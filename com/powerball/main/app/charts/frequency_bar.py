from datetime import datetime
import streamlit as st
from com.powerball.main.utility.common_utilities import CommonUtilities
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase

class FrequencyChartGenerator(LotteryChartBase):
    def __init__(self, data, start_date=None, end_date=None, chart_name="Chart"):
        self.main_numbers = []
        self.special_numbers = []
        # Initialize parent (which runs process_data automatically)
        super().__init__(data, start_date, end_date, chart_name)

    def extract_numbers(self, numbers):
        """
        IMPLEMENTATION: Groups 0-4 as 'Main' and 5 as 'Special'
        """
        self.main_numbers.extend(numbers[:5])
        self.special_numbers.append(numbers[5])

    def plot(self, plot_type='main', figsize=(6, 4)):
        if plot_type == 'main':
            return self.generate_plot(self.main_numbers, "Main", 'skyblue', figsize)
        else:
            return self.generate_plot(self.special_numbers, "Powerball", 'salmon', figsize)


# --- DASHBOARD RUNNER (Remains mostly unchanged, just calls the class) ---
def run_dashboard(input_data):
    st.set_page_config(page_title="Lottery Dashboard", layout="wide")

    # This prevents the "Zoom Out = Giant Chart" effect.
    st.markdown(
        """
        <style>
            /* Target the main Streamlit container */
            .block-container {
                max-width: 2400px; /* <--- ADJUST THIS PIXEL VALUE IF NEEDED */
                padding-left: 2rem;
                padding-right: 2rem;
                margin: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📊 Lottery Frequency Dashboard")

    # --- 1. LOAD CONFIG ---
    try:
        min_date = datetime.strptime(CommonUtilities.get_from_config("min_date"), "%m-%d-%Y").date()
        max_date = datetime.strptime(CommonUtilities.get_from_config("max_date"), "%m-%d-%Y").date()
    except Exception as e:
        st.error(f"Error reading dates from config: {e}")
        st.stop()

    # --- 2. SIDEBAR LOGIC ---
    st.sidebar.header("⚙️ Settings")
    global_override = st.sidebar.checkbox("Override All Date Filters", value=True)
    global_start, global_end = None, None

    if global_override:
        st.sidebar.write("Global range active:")
        global_range = st.sidebar.slider(
            "Select Global Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
        global_start, global_end = global_range
    else:
        st.sidebar.info("Using individual chart filters.")

    # --- 3. HELPER FOR SLIDERS ---
    def get_dates(key_id):
        if global_override:
            return global_start, global_end

        st.write(f"**Filter for {key_id}:**")
        slider = st.slider(
            f"Range ({key_id})",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            key=key_id
        )
        return slider[0], slider[1]

    # --- 4. RENDER CHARTS ---
    # --- LAYOUT: 60% / 40% SPLIT COLUMNS ---
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        st.subheader("Main Numbers")
        d1_start, d1_end = get_dates("Main Numbers")
        gen1 = FrequencyChartGenerator(
            input_data,
            start_date=d1_start.strftime("%m-%d-%Y"),
            end_date=d1_end.strftime("%m-%d-%Y"),
            chart_name="Main Numbers"
        )
        # 1. Generate the figure
        fig1 = gen1.plot('main', figsize=(9, 3.5))

        # 2. Render with dynamic width
        st.pyplot(fig1, width='stretch')

    with col2:
        st.subheader("Powerball")
        d2_start, d2_end = get_dates("Powerball")
        gen2 = FrequencyChartGenerator(
            input_data,
            start_date=d2_start.strftime("%m-%d-%Y"),
            end_date=d2_end.strftime("%m-%d-%Y"),
            chart_name="Powerball"
        )
        # 1. Generate the figure
        fig2 = gen2.plot('special', figsize=(6, 3.5))

        # 2. Render with dynamic width
        st.pyplot(fig2, width='stretch')