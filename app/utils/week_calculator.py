"""Week type calculation utilities"""

from datetime import date
from app.config import settings


def get_week_type(current_date: date | None = None) -> str:
    """
    Calculate the current week type (ODD or EVEN) based on academic start date.
    
    Args:
        current_date: Date to calculate for (defaults to today)
    
    Returns:
        "ODD" or "EVEN"
    """
    if current_date is None:
        current_date = date.today()
    
    start_date = settings.academic_start_date
    delta = current_date - start_date
    week_number = delta.days // 7 + 1
    return "ODD" if week_number % 2 != 0 else "EVEN"
