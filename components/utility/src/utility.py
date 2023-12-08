from datetime import datetime, timedelta
import calendar


def calculate_timespan(days_ahead: int) -> (list[int], dict[str, int], list[datetime]):
    assert(days_ahead > 0)

    current = datetime.now().date()
    dates = [current]
    days = [current.day]
    months = {current.strftime("%B %Y"): (calendar.monthrange(current.year, current.month)[1] - current.day + 1)}

    for i in range(days_ahead):
        current += timedelta(days=1)
        dates.append(current)
        days.append(current.day)
        if current.day == 1:
            months[current.strftime("%B %Y")] = calendar.monthrange(current.year, current.month)[1]

    months[current.strftime("%B %Y")] = current.day

    return days, months, dates
