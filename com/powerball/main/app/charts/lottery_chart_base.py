from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from com.powerball.main.utility.common_utilities import CommonUtilities


class LotteryChartBase:
    def __init__(self, data, start_date=None, end_date=None, chart_name="Chart"):
        self.raw_data = data
        self.chart_name = chart_name

        # --- SHARED: Date Parsing Logic ---
        if start_date:
            self.start_date = datetime.strptime(start_date, "%m-%d-%Y")
        else:
            self.start_date = datetime.min

        if end_date:
            self.end_date = datetime.strptime(end_date, "%m-%d-%Y")
        else:
            self.end_date = datetime.max

        # Trigger the processing (which child classes will use)
        self.process_data()

    def process_data(self):
        """
        SHARED: Loops through the years and dates.
        Delegates the specific number extraction to the child class via `extract_numbers`.
        """
        for year, draws in self.raw_data.items():
            for draw_record in draws:
                for date_str, numbers in draw_record.items():
                    current_date = datetime.strptime(date_str, "%m-%d-%Y")

                    # Date Filter applies to everyone
                    if self.start_date <= current_date <= self.end_date:
                        # This method must be defined in the child class
                        self.extract_numbers(numbers)

    def extract_numbers(self, numbers):
        """ Child classes must overwrite this to save data their own way. """
        raise NotImplementedError("Child classes must implement extract_numbers")

    def generate_plot(self, data_list, title_suffix, color, figsize=(6, 4)):
        """
        SHARED: The plotting logic.
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=CommonUtilities.get_chart_dpi())

        if not data_list:
            ax.text(0.5, 0.5, "No data found in range", ha='center', va='center')
            return fig

        counts = pd.Series(data_list).value_counts().sort_index()

        ax.bar(counts.index, counts.values, color=color, edgecolor='black')

        # Format dates for title
        s_txt = self.start_date.strftime('%m-%d-%Y') if self.start_date != datetime.min else "Start"
        e_txt = self.end_date.strftime('%m-%d-%Y') if self.end_date != datetime.max else "End"

        ax.set_title(f"{self.chart_name} ({title_suffix})\nRange: {s_txt} to {e_txt}")
        ax.set_xlabel("Ball Number")
        ax.set_ylabel("Frequency")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_xticks(counts.index)

        # Optimize tick labels based on chart size
        tick_size = 7 if figsize[0] < 6 else 8
        ax.tick_params(axis='x', rotation=90, labelsize=tick_size)

        plt.tight_layout()
        return fig
