#This file includes helper methods used by other pi2golite files

def validate_max(value, maxv=100):
    if value > maxv:
        value = maxv
    elif value < 0:
        value = 0
    return value
