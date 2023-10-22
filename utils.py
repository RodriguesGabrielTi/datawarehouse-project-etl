from numpy import NaN
import re

def to_float(value):
    if type(value, NaN):
        return 0
    float(value)


def extract_float(value: str):
    # Regular expression to match a float number
    match = re.search(r'(\d+\.\d+)', value)
    if match:
        return float(match.group(1))
    else:
        return None
