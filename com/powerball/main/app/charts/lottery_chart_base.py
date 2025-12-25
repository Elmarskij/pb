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

    def get_base_chart(self, source_df, title, color_hex, date_param):
        """
        Creates a single Altair Bar Chart with Real-Time Filtering.
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
            title=alt.TitleParams(
                title,
                color='#000000',
                fontSize=20,
                anchor='middle',
                fontWeight='bold'
            ),
            height=400,  # Fixed Height 400px
            width=450,   # Fixed Width
            background='#dbd9d9'
        ).configure_axis(
            labelColor='black',    # Set X and Y value colors
            titleColor='black',    # Set X and Y title colors
        ).add_params(
            date_param   # Bind the slider to this chart
        ).transform_filter(
            # REAL-TIME FILTER: Filter based on Day Integer
            alt.datum.ts_days >= date_param
        )

        return chart
