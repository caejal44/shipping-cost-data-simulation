from datetime import date, timedelta
import random

def sample_ship_date():
    """generate ship date for a shipment. Returns a date object"""
    start_date = date(2024, 1, 1)
    end_date = date.today()

    # select random interval from start date
    time_between = (end_date - start_date).days
    random_days = random.randint(0, time_between)

    return start_date + timedelta(days=random_days)

def sample_weight_kg():
    """generate weight in kg for each shipment with a right-skewed distribution. Returns an integer weight"""
    weight = random.lognormvariate(5, 0.75)
    weight = max(weight, 10)
    weight = min(weight, 5000)
    return int(round(weight))

def sample_service(miles: float) -> str:
    """ selects eligible service for shipment based on miles with realistic weighting. Returns a string"""
    if miles < 1500:
        services = ["Express", "Expedited", "Standard"]
        weights = [0.10, 0.20, 0.70]
    else:
        services = ["Express", "Standard"]
        weights = [0.07, 0.93]
    return random.choices(services, weights=weights, k=1)[0]

def sample_delivery_status():
    """ returns delivery status for a shipment: Returns a string"""
    delivery_status = ["Delivered", "Missing", "Returned"]
    weights = [0.96, 0.03, 0.01]
    return random.choices(delivery_status, weights=weights, k=1)[0]

