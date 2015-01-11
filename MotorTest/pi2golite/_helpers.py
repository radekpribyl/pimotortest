#This file includes helper methods used by other pi2golite files

def validate_max100( value ):
    if value > 100:
        value = 100
    elif value < 0:
        value = 0
    return value