def convert_to_12_hour_format(hour):
    if hour > 12:
        hour = hour - 12
    elif hour == 0:
        hour = 12
    return hour
