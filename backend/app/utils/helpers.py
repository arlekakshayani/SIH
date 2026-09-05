from datetime import datetime, date

def format_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")

def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()
