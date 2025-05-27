from datetime import datetime


def is_expired(date_str: str) -> bool:
    """
    Checks if the given date is expired compared to the current time.

    Parameters:
    - date_str (str): Date in the format "YYYY-MM-DD HH:MM:SS"

    Returns:
    - bool: True if expired, False otherwise
    """
    given_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    return given_date < now


# Example usage
date = "2026-03-14 00:00:00"
if is_expired(date):
    print("Date is expired")
else:
    print("Date is still valid")
