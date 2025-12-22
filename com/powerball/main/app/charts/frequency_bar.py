import streamlit as st
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase
from com.powerball.main.utility.dashboard_utilities import render_chart_in_column


class FrequencyChartGenerator(LotteryChartBase):
    def __init__(self, df_data, start_date=None, end_date=None, chart_name="Chart"):
        self.main_numbers = []
        self.special_numbers = []
        super().__init__(df_data, start_date, end_date, chart_name)

    def extract_numbers_from_df(self):
        """
        OPTIMIZED: Grab columns directly.
        """
        if self.filtered_df.empty:
            return

        # 1. Main Numbers: Columns n1 through n5
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']
        self.main_numbers = self.filtered_df[main_cols].values.flatten().tolist()

        # 2. Powerball: Column pb
        self.special_numbers = self.filtered_df['pb'].tolist()

    def plot(self, plot_type='main', figsize=(6, 4)):
        if plot_type == 'main':
            return self.generate_plot(self.main_numbers, "Main", 'skyblue', figsize)
        else:
            return self.generate_plot(self.special_numbers, "Powerball", 'salmon', figsize)


# --- EXPOSED RENDER FUNCTION ---
def render_main_section(input_data, min_d, max_d, global_state):
    """
    Renders the top section (Main Numbers + Powerball).
    """
    st.header("Main & Powerball Frequency")
    col1, col2 = st.columns([0.6, 0.4])

    # Column 1: Main Numbers
    render_chart_in_column(
        column_obj=col1,
        title="Main Numbers",
        data=input_data,
        GeneratorClass=FrequencyChartGenerator,
        min_d=min_d, max_d=max_d,
        global_state=global_state,
        figsize=(9, 3.5),  # Wider figure for 60% column
        plot_kwargs={'plot_type': 'main'}
    )

    # Column 2: Powerball
    render_chart_in_column(
        column_obj=col2,
        title="Powerball",
        data=input_data,
        GeneratorClass=FrequencyChartGenerator,
        min_d=min_d, max_d=max_d,
        global_state=global_state,
        figsize=(6, 3.5),  # Normal figure for 40% column
        plot_kwargs={'plot_type': 'special'}
    )
