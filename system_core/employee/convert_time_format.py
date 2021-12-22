from math import floor

def convert_to_hhmm(time):
    hours = int(floor(time))
    decimal = (time - hours) / 0.60

    hour_decimal = hours + decimal

    return hour_decimal
