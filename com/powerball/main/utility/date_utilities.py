# date_utils.py
from datetime import datetime, timedelta, date
import pytz


class DateUtilities:
    """
    Determines the next valid lottery draw date (Mon, Wed, Sat)
    considering a 9 PM CST cut-off time.
    """
    CST = pytz.timezone('America/Chicago')
    CUT_OFF_HOUR: int = 21  # 9 PM (21:00)
    # Weekday mapping: Monday=0, Wednesday=2, Saturday=5
    TARGET_DAYS: list[int] = [0, 2, 5] # Monday, Wednesday, Saturday

    def get_target_date(self) -> date:
        """Calculates and returns the target date object."""
        now_utc = datetime.now(pytz.utc)
        now_cst = now_utc.astimezone(self.CST)

        current_date_to_check: date = now_cst.date()

        # Check if today's drawing has passed the cut-off
        if now_cst.weekday() in self.TARGET_DAYS and now_cst.hour >= self.CUT_OFF_HOUR:
            # If past cut-off on a draw day, start looking from tomorrow
            current_date_to_check += timedelta(days=1)

        return self._find_next_target_day(current_date_to_check)

    def _find_next_target_day(self, start_date: date) -> date:
        """Helper method to iterate until a target day is found."""
        while start_date.weekday() not in self.TARGET_DAYS:
            start_date += timedelta(days=1)
        return start_date
