from datetime import datetime, timedelta

def parse_date(date_str):
    """
    Parses a relative date string from Google News into a YYYY-MM-DD format.
    """
    today = datetime.today()
    date_str = date_str.lower()
    
    if "today" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "yesterday" in date_str:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "hours ago" in date_str or "minutes ago" in date_str:
        return today.strftime("%Y-%m-%d")
    else:
        try:
            # Try parsing formats like "Nov 29, 2023"
            parsed_date = datetime.strptime(date_str, "%b %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            # Fallback for other unhandled formats
            return today.strftime("%Y-%m-%d")
