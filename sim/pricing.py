import random
import pandas as pd

def get_rate_per_mile(miles: float, carrier_id: str, mile_df: pd.DataFrame) -> float:
    """gets rate per mile per carrier. Returns a float"""
    carrier_mile_df = mile_df[mile_df["carrier_id"] == carrier_id]
    mile_rate = carrier_mile_df[carrier_mile_df["determinant"] >= miles].sort_values("determinant")
    if mile_rate.empty:
        raise ValueError(f"No mile tier found for carrier_id={carrier_id}, miles={miles}")
    return float(mile_rate.iloc[0]["value"])

def get_rate_per_weight(weight: float, carrier_id: str, weight_df: pd.DataFrame) -> float:
    """gets weight rate per kg per carrier. Returns a float"""
    carrier_weight_df = weight_df[weight_df["carrier_id"] == carrier_id]
    weight_rate = carrier_weight_df[carrier_weight_df["determinant"] >= weight].sort_values("determinant")
    if weight_rate.empty:
        raise ValueError(f" No weight found for carrier_id={carrier_id}, weight={weight}")
    return float(weight_rate.iloc[0]["value"])

def get_service_multiplier(service: str, carrier_id: str, service_df:pd.DataFrame) -> float:
    """gets service multiplier per carrier. Returns a float"""
    carrier_service_df = service_df[service_df["carrier_id"] == carrier_id]
    service_multiplier = carrier_service_df[carrier_service_df["determinant"] == service]
    if service_multiplier.empty:
        raise ValueError(f"No service multiplier found for carrier_id={carrier_id}, service={service}")
    return float(service_multiplier.iloc[0]["value"])

def get_fuel_rate(service: str, carrier_id: str, fuel_df: pd.DataFrame) -> float:
    """gets fuel rate per carrier service. Returns a float"""
    fuel_rate_df = fuel_df[fuel_df["carrier_id"] == carrier_id]
    fuel_rate = fuel_rate_df[fuel_rate_df["determinant"] == service]
    if fuel_rate.empty:
        raise ValueError(f"No fuel rate found for carrier_id={carrier_id}, service={service}")
    return float(fuel_rate.iloc[0]["value"])

def sample_price_variation():
    """Sample price variation for invoice-level noise"""
    return random.uniform(0.98, 1.02)

def calculate_price(miles: float, weight: float, mile_rate: float, weight_rate: float, service_multiplier: float,
                    fuel_rate: float, price_variation: float) -> float:
    """calculates the price of the shipment. Returns a float"""
    mile_cost = miles * mile_rate
    weight_cost = weight * weight_rate
    base_cost = mile_cost + weight_cost
    adjusted_cost = base_cost * service_multiplier * fuel_rate * price_variation
    return round(adjusted_cost,2)

def price_row (row: pd.Series, mile_df: pd.DataFrame, weight_df: pd.DataFrame, service_df:
               pd.DataFrame, fuel_df: pd.DataFrame) -> float:
    mile_row_rate = get_rate_per_mile(row["miles"], row["carrier_id"], mile_df)
    weight_row_rate = get_rate_per_weight(row["weight"], row["carrier_id"], weight_df)
    service_multiplier = get_service_multiplier(row["service"], row["carrier_id"], service_df)
    fuel_row_rate = get_fuel_rate(row["service"], row["carrier_id"], fuel_df)
    price_row_variation = sample_price_variation()
    return calculate_price(row["miles"], row["weight"], mile_row_rate, weight_row_rate,service_multiplier, fuel_row_rate, price_row_variation)



