import pandas as pd
import altair as alt
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase


class FrequencyChartGenerator(LotteryChartBase):
    def prepare_altair_data(self):
        if self.df_data.empty:
            return {'main': pd.DataFrame(), 'special': pd.DataFrame()}

        # 1. Main Numbers
        main_cols = ['n1', 'n2', 'n3', 'n4', 'n5']

        df_main = self.df_data.melt(
            id_vars=[],  # No ID vars needed for simple count
            value_vars=main_cols,
            value_name='Number'
        ).drop(columns=['variable'])

        # 2. Powerball
        df_special = self.df_data[['pb']].rename(columns={'pb': 'Number'})

        return {'main': df_main, 'special': df_special}

    def build_section(self):
        chart_main = self.get_base_chart(
            self.long_data['main'], "Main Numbers", '#87CEEB'
        )
        chart_pb = self.get_base_chart(
            self.long_data['special'], "Powerball", '#FA8072'
        )

        combined = alt.hconcat(
            chart_main,
            chart_pb
        ).resolve_scale(
            y='shared'
        ).properties(
            title="Main & Powerball Frequency"
        )

        return combined
