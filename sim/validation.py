import pandas as pd

def output_check(shipment_df):
    """quality check on final dataframe"""
    if shipment_df["shipment_id"].isna().any():
        raise ValueError(f"Missing shipment ids")
    if (shipment_df["cost"] <= 0).any():
        raise ValueError(f"A Shipment has an invalid cost")
    if (shipment_df["miles"] <= 0).any():
        raise ValueError(f"A shipment has no or negative miles")
    if shipment_df["miles"].isna().any():
        raise ValueError(f"Missing miles from a shipment")
    if ((shipment_df["status"] == "Delivered") & (shipment_df["ship_date"] > shipment_df["delivery_date"])).any():
        raise ValueError(f"A shipment has a delivery date less than ship date")
    if ((shipment_df["service"] == "Expedited") & (shipment_df["miles"] >= 1500)).any():
        raise ValueError(f"Shipment has a service of expedited with a mileage greater than 1500")
    if shipment_df["carrier_id"].isna().any():
        raise ValueError(f"Missing carrier id from a shipment")
    if shipment_df["origin_warehouse"].isna().any():
        raise ValueError(f"Missing origin warehouse from a shipment")
    if shipment_df["destination_store"].isna().any():
        raise ValueError(f"Missing destination store from a shipment")

def summary_stats(shipment_df):
    """creates summary statistics of shipment dataframe"""
    total_count = shipment_df["shipment_id"].count()
    print(f"Total count of shipments: {total_count}")
    shipments_lane = shipment_df[["origin_warehouse", "destination_store"]].value_counts()
    print(f"Shipments per lane:")
    print(shipments_lane)
    shipments_carrier = shipment_df["carrier_id"].value_counts()
    print(f"Shipments per carrier id:")
    print(shipments_carrier)
    cost_percentiles = shipment_df["cost"].quantile(q=[0.05,0.25,0.50,0.75,0.95])
    print(cost_percentiles)
    transit_percentiles = shipment_df["transit_days"].quantile(q=[0.05,0.25,0.5,0.75,0.95])
    print(transit_percentiles)
    shipment_min = shipment_df["cost"].min()
    print(f"Shipment min cost: {shipment_min}")
    shipment_status = shipment_df["status"].value_counts()
    print(f"Shipment status: {shipment_status}")
    transit_miles = shipment_df.groupby(pd.cut(shipment_df["miles"],5))["transit_days"].mean()
    print(f"Transit miles: {transit_miles}")
    delivery_date_sum = shipment_df[shipment_df["status"] != "Delivered"]["delivery_date"].notna().sum()
    print(f"Delivery date sum (should be 0): {delivery_date_sum}")
    transit_day_sum = shipment_df[shipment_df["status"] != "Delivered"]["transit_days"].notna().sum()
    print(f"Transit day sum (should be 0): {transit_day_sum}")
    missing_carriers = shipment_df["carrier_id"].isna().sum()
    print(f"Missing carriers (should be 0): {missing_carriers}")

