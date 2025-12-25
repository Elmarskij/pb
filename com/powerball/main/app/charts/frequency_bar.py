import pandas as pd
import altair as alt
from com.powerball.main.app.charts.lottery_chart_base import LotteryChartBase


class FrequencyChartGenerator(LotteryChartBase):
    def prepare_altair_data(self):
        if self.df_data.empty:
            return {'main': pd.DataFrame(), 'special': pd.DataFrame()}

        # Keep ts_days for filtering
        main_cols = ['ts_days', 'n1', 'n2', 'n3', 'n4', 'n5']

        df_main = self.df_data[main_cols].melt(
            id_vars=['ts_days'], # Preserve ID for filter
            value_vars=['n1', 'n2', 'n3', 'n4', 'n5'],
            value_name='Number'
        ).drop(columns=['variable'])

        # Keep ts_days for filtering
        df_special = self.df_data[['ts_days', 'pb']].rename(columns={'pb': 'Number'})

        return {'main': df_main, 'special': df_special}

    def build_section(self, date_param):
        chart_main = self.get_base_chart(
            self.long_data['main'], "Main Numbers", '#87CEEB', date_param
        )
        chart_pb = self.get_base_chart(
            self.long_data['special'], "Powerball", '#FA8072', date_param
        )

        return chart_main, chart_pb
