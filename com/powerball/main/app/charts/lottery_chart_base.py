import altair as alt
import pandas as pd


class LotteryChartBase:
    def __init__(self, df_data: pd.DataFrame, chart_name="Chart"):
        self.df_data = df_data
        self.chart_name = chart_name
        self.long_data = self.prepare_altair_data()

    def prepare_altair_data(self):
        """Child classes must implement this to return a DataFrame optimized for Altair."""
        raise NotImplementedError

    def get_base_chart(self, source_df, title, color_hex):
        """
        Creates a single Altair Bar Chart.
        """
        chart = alt.Chart(source_df).mark_bar(
            color=color_hex,
            stroke='black',
            strokeWidth=0.5
        ).encode(
            x=alt.X('Number:O', title='Ball', sort='ascending'),
            y=alt.Y('count()', title=None),
            tooltip=['Number', 'count()']
        ).properties(
            title=title,
            height=200,
            width='container'
        )

        return chart
