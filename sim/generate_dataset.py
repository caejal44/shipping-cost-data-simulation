import random

import pandas as pd
import numpy as np
import pathlib

from sim.export import prepare_for_export, export_shipment_csv
from sim.loaders import load_carrier_route_matrix
from sim.loaders import load_carrier_matrix
from sim.loaders import load_lane_id_route
from sim.loaders import load_pricing
from sim import lane_model
from sim.pricing import price_row
from sim.sampling import sample_ship_date, sample_service, sample_delivery_status, sample_weight_kg
from sim.transit import calculate_transit_days, get_delivery_date
from sim.validation import output_check, summary_stats

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data_inputs"

def main():
    random.seed(42)
    np.random.seed(42)
    carrier_df = load_carrier_matrix(DATA_PATH / "carrier_matrix.csv")
    lane_df = load_lane_id_route(DATA_PATH / "lane_id_route.csv")
    carrier_route_df = load_carrier_route_matrix(DATA_PATH / "carrier_route_matrix.csv")
    pricing_dict = load_pricing(DATA_PATH / "pricing.csv")

    # unpack pricing dict into dataframes
    mile_df = pricing_dict["mile"]
    weight_df = pricing_dict["weight"]
    service_df = pricing_dict["service"]
    fuel_df = pricing_dict["fuel"]

    # create lane-carrier dataframe with route information per carrier
    lane_carrier_df = lane_model.build_lane_carrier_df(lane_df, carrier_route_df)

    # generate required number of route-carrier combinations
    number_of_copies = 53
    columns_to_copy = ["lane_id", "carrier_id", "origin_warehouse", "destination_store", "miles"]

    seed_df = lane_carrier_df[columns_to_copy]
    shipment_df = seed_df.loc[seed_df.index.repeat(number_of_copies)].reset_index(drop=True)

    # generate distance-based subsets for random selection
    city_mile_df = seed_df[seed_df["miles"] <= 30]
    low_mile_df = seed_df[(seed_df["miles"] <= 500) & (seed_df["miles"] > 30)]
    mid_mile_df = seed_df[(seed_df["miles"] <= 1000) & (seed_df["miles"] > 500)]
    high_mile_df = seed_df[(seed_df["miles"] <= 1500) & (seed_df["miles"] > 1000)]
    long_mile_df = seed_df[seed_df["miles"] > 1500]

    # ensure dataframes are not empty
    if city_mile_df.empty:
        raise ValueError("City miles dataframe is empty")
    if high_mile_df.empty:
        raise ValueError("High miles dataframe is empty")
    if low_mile_df.empty:
        raise ValueError("Low miles dataframe is empty")
    if mid_mile_df.empty:
        raise ValueError("Mid miles dataframe is empty")
    if long_mile_df.empty:
        raise ValueError("Long miles dataframe is empty")

    # create weighted random selection to add to shipment_df
    routes = [city_mile_df, low_mile_df, mid_mile_df, high_mile_df, long_mile_df]
    weights = [0.02, 0.40, 0.33, 0.15, 0.10]
    sample_choices = 65000
    random_row_list = []

    for _ in range(sample_choices):
        sample_df = random.choices(routes, weights=weights, k=1)[0]
        random_row = sample_df.sample(1).iloc[0]
        random_row_list.append(random_row)

    temp_df = pd.DataFrame(random_row_list, columns=["lane_id", "carrier_id", "origin_warehouse", "destination_store", "miles"])
    shipment_df = pd.concat([shipment_df, temp_df], ignore_index = True, axis=0)

    # insert blank columns into shipment dataframe
    shipment_df.insert(0,"shipment_id", None)
    shipment_df[["status", "ship_date", "delivery_date", "service", "weight", "cost", "transit_days"]] = None

    # generate values for empty columns
    shipment_df["shipment_id"] = pd.RangeIndex(start=1001, stop=1001 + len(shipment_df)).astype(str)
    shipment_df["service"] = shipment_df["miles"].apply(sample_service)
    shipment_df["status"] = [sample_delivery_status() for _ in range(len(shipment_df))]
    shipment_df["weight"] = [sample_weight_kg() for _ in range(len(shipment_df))]
    shipment_df["ship_date"] = [sample_ship_date() for _ in range(len(shipment_df))]
    shipment_df["transit_days"] = shipment_df.apply(lambda r: calculate_transit_days(r["status"], r["service"], r["miles"]), axis=1)
    shipment_df["delivery_date"] = shipment_df.apply(lambda r: get_delivery_date(r["ship_date"], r["transit_days"]), axis=1)

    # generate cost for each shipment
    shipment_df["cost"] = shipment_df.apply(lambda r: price_row(r, mile_df,weight_df,service_df,fuel_df), axis=1)

    # run quality checks
    output_check(shipment_df)
    summary_stats(shipment_df)

    # prepare and run export
    shipment_df = prepare_for_export(shipment_df, carrier_df)
    export_shipment_csv(shipment_df)

if __name__ == "__main__":
    main()
