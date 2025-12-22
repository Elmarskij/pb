import streamlit as st
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase
from com.powerball.main.utility.dashboard_utilities import render_chart_in_column


class IndividualFrequencyChartGenerator(LotteryChartBase):
    def __init__(self, df_data, start_date=None, end_date=None, chart_name="Positions"):
        self.positions = {i: [] for i in range(6)}
        super().__init__(df_data, start_date, end_date, chart_name)

    def extract_numbers_from_df(self):
        if self.filtered_df.empty:
            return

        # Map DataFrame columns to Position Index 0-5
        col_map = {0: 'n1', 1: 'n2', 2: 'n3', 3: 'n4', 4: 'n5', 5: 'pb'}

        for i in range(6):
            col_name = col_map[i]
            self.positions[i] = self.filtered_df[col_name].tolist()

    def plot(self, position_index, color='skyblue', figsize=(6, 4)):
        data = self.positions.get(position_index, [])
        return self.generate_plot(data, f"Space {position_index + 1}", color, figsize)


# --- EXPOSED RENDER FUNCTION ---
def render_individual_section(input_data, min_d, max_d, global_state):
    """
    Renders the grid of 6 individual number charts.
    """
    st.header("Lottery Individual Numbers Frequency")

    colors = ['#d62728', '#ff7f0e', '#ffd700', '#2ca02c', '#1f77b4', '#9467bd']

    # Loop to create rows of 2 charts
    for i in range(0, 6, 2):
        col1, col2 = st.columns(2)

        # Chart for Space i (Left Column)
        render_chart_in_column(
            column_obj=col1,
            title=f"Space {i + 1}",
            data=input_data,
            GeneratorClass=IndividualFrequencyChartGenerator,
            min_d=min_d, max_d=max_d,
            global_state=global_state,
            figsize=(6, 2.5),  # Reduced height as requested
            plot_kwargs={'position_index': i, 'color': colors[i]}
        )

        # Chart for Space i+1 (Right Column, if exists)
        if i + 1 < 6:
            render_chart_in_column(
                column_obj=col2,
                title=f"Space {i + 2}",
                data=input_data,
                GeneratorClass=IndividualFrequencyChartGenerator,
                min_d=min_d, max_d=max_d,
                global_state=global_state,
                figsize=(6, 2.5),  # Reduced height as requested
                plot_kwargs={'position_index': i + 1, 'color': colors[i + 1]}
            )

        st.markdown("---")
