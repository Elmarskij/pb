import pandas as pd
import altair as alt
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase


class IndividualFrequencyChartGenerator(LotteryChartBase):
    def prepare_altair_data(self):
        position_dfs = {}
        if self.df_data.empty:
            return position_dfs

        col_map = {0: 'n1', 1: 'n2', 2: 'n3', 3: 'n4', 4: 'n5', 5: 'pb'}
        for i in range(6):
            col_name = col_map[i]
            # Include ts_days for filtering
            position_dfs[i] = self.df_data[['ts_days', col_name]].rename(columns={col_name: 'Number'})
        return position_dfs

    def build_section(self, date_param):
        colors = ['#d62728', '#ff7f0e', '#ffd700', '#2ca02c', '#1f77b4', '#9467bd']

        chart_list = []

        for i in range(6):
            title = f"Space {i + 1}"
            chart = self.get_base_chart(
                self.long_data[i], title, colors[i], date_param
            )
            chart_list.append(chart)

        return chart_list
