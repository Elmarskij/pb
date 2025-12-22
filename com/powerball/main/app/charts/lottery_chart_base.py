import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, date
from com.powerball.main.utility.common_utilities import CommonUtilities


class LotteryChartBase:
    def __init__(self, df_data: pd.DataFrame, start_date=None, end_date=None, chart_name="Chart"):
        self.df_data = df_data  # Stores the full DataFrame
        self.chart_name = chart_name
        self.filtered_df = pd.DataFrame()  # Will hold cut data

        # Parse filter dates - ROBUST HANDLING
        # Handles both strings (from legacy code) and date objects (from new slider)
        if start_date:
            if isinstance(start_date, (datetime, date)):
                self.start_date = pd.to_datetime(start_date)
            else:
                self.start_date = datetime.strptime(str(start_date), "%m-%d-%Y")
        else:
            self.start_date = pd.to_datetime(datetime.min)

        if end_date:
            if isinstance(end_date, (datetime, date)):
                self.end_date = pd.to_datetime(end_date)
            else:
                self.end_date = datetime.strptime(str(end_date), "%m-%d-%Y")
        else:
            self.end_date = pd.to_datetime(datetime.max)

        self.process_data()

    def process_data(self):
        """
        OPTIMIZED: Uses Vectorized Pandas Filtering.
        """
        if self.df_data.empty:
            return

        # Ensure 'Date' column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df_data['Date']):
             self.df_data['Date'] = pd.to_datetime(self.df_data['Date'])

        # Filter
        mask = (self.df_data['Date'] >= self.start_date) & (self.df_data['Date'] <= self.end_date)
        self.filtered_df = self.df_data.loc[mask]

        # Trigger extraction hook
        self.extract_numbers_from_df()

    def extract_numbers_from_df(self):
        """Child classes must implement this to grab columns from self.filtered_df"""
        raise NotImplementedError("Child classes must implement extract_numbers_from_df")

    def generate_plot(self, data_list, title_suffix, color, figsize=(6, 4)):
        current_dpi = CommonUtilities.get_chart_dpi()
        fig, ax = plt.subplots(figsize=figsize, dpi=current_dpi)

        if not data_list:
            ax.text(0.5, 0.5, "No data found in range", ha='center', va='center')
            return fig

        counts = pd.Series(data_list).value_counts().sort_index()
        ax.bar(counts.index, counts.values, color=color, edgecolor='black')
        ax.set_title(f"{self.chart_name} ({title_suffix})", fontsize=11)
        ax.set_xlabel("Ball Number", fontsize=8)
        ax.set_ylabel("Frequency", fontsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
        ax.set_xticks(counts.index)
        tick_size = 7 if figsize[0] < 6 else 8
        ax.tick_params(axis='x', rotation=90, labelsize=tick_size)
        plt.tight_layout()
        return fig
