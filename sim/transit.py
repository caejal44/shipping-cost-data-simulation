from datetime import timedelta
import random
from json.decoder import NaN
import pandas as pd


def calculate_transit_days(delivery_status, service, miles):
    """ returns transit for a shipment based on delivery status, service, and miles. Returns an int OR none"""
    if delivery_status != "Delivered":
        return None

    if service == "Express":
        if miles <= 30:
            days = [1,2,3]
            weights = [0.85, 0.10, 0.05]
        else:
            days = [1,2,3,4,5]
            weights = [0.50, 0.35, 0.10, 0.03, 0.02]
        return random.choices(days, weights=weights, k=1)[0]

    elif service == "Expedited":
        if miles <= 30:
            days = [1,2,3]
            weights = [0.70, 0.18, 0.12]
        elif miles <= 500:
            days = [1,2,3,4,5,6]
            weights = [0.35, 0.30, 0.25, 0.13, 0.06, 0.01]
        elif miles <= 1000:
            days = [2,3,4,5,6,7]
            weights = [0.35, 0.30, 0.25, 0.13, 0.06, 0.01]
        elif miles < 1500:
            days = [3, 4, 5, 6, 7, 8]
            weights = [0.35, 0.30, 0.25, 0.13, 0.06, 0.01]
        else:
            raise ValueError("Expedited Service not allowed for miles >= 1500")
        return random.choices(days, weights=weights, k=1)[0]
    elif service == "Standard":
        if miles <= 30:
            days = [1,2,3,4]
            weights = [0.65, 0.20, 0.10, 0.05]
        elif miles <= 500:
            days = [1, 2, 3, 4, 5, 6, 7, 8]
            weights = [0.30, 0.35, 0.15, 0.10, 0.05, 0.03, 0.01, 0.01]
        elif miles <= 1000:
            days = [2,3,4,5,6,7,8,9]
            weights = [0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.01, 0.01]
        elif miles <= 1500:
            days = [3,4,5,6,7,8,9,10]
            weights = [0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.01, 0.01]
        elif miles <= 2000:
            days = [4,5,6,7,8,9,10,11]
            weights = [0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.01, 0.01]
        elif miles <= 2500:
            days = [5,6,7,8,9,10,11,12]
            weights = [0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.01, 0.01]
        else:
            days = [6,7,8,9,10,11,12,13]
            weights = [0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.01, 0.01]
        return random.choices(days, weights=weights, k=1)[0]
    else:
        raise ValueError(f"Unknown service: {service}")

def get_delivery_date(ship_date, transit_days):
    """calculates delivery date based on shipment date and transit. Returns a date or none"""
    if pd.isna(transit_days):
        return None
    if transit_days < 0:
        raise ValueError("transit_days cannot be negative")
    return ship_date + timedelta(days=int(transit_days))
