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
            position_dfs[i] = self.df_data[[col_name]].rename(columns={col_name: 'Number'})
        return position_dfs

    def build_section(self):
        colors = ['#d62728', '#ff7f0e', '#ffd700', '#2ca02c', '#1f77b4', '#9467bd']

        rows = []
        for i in range(0, 6, 2):
            c1 = self.get_base_chart(
                self.long_data[i], f"Space {i + 1}", colors[i]
            )

            if i + 1 < 6:
                c2 = self.get_base_chart(
                    self.long_data[i + 1], f"Space {i + 2}", colors[i + 1]
                )
                row = alt.hconcat(c1, c2).resolve_scale(y='shared')
            else:
                row = c1

            rows.append(row)

        final_grid = alt.vconcat(*rows).properties(
            title="Individual Position Frequency"
        )

        return final_grid
