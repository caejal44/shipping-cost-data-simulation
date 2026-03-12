import pandas as pd
import pathlib

def prepare_for_export(shipment_df: pd.DataFrame, carrier_df: pd.DataFrame) -> pd.DataFrame:
    """reorders and cleans columns before exporting data"""
    shipment_df_copy = shipment_df.copy()
    lookup_series = carrier_df.set_index("carrier_id")["carrier_name"]
    shipment_df_copy["carrier"] = shipment_df_copy["carrier_id"].map(lookup_series)
    shipment_df_copy["ship_date"] = pd.to_datetime(shipment_df_copy["ship_date"], errors="coerce")
    shipment_df_copy["ship_date"] = shipment_df_copy["ship_date"].dt.strftime("%m/%d/%Y")
    shipment_df_copy["delivery_date"] = pd.to_datetime(shipment_df_copy["delivery_date"], errors="coerce")
    shipment_df_copy["delivery_date"] = shipment_df_copy["delivery_date"].dt.strftime("%m/%d/%Y")

    new_order = ["shipment_id", "origin_warehouse", "destination_store", "carrier", "service", "status", "ship_date", "delivery_date",
                 "weight", "transit_days", "miles", "cost", "lane_id", "carrier_id"]
    shipment_df_copy = shipment_df_copy[new_order]
    shipment_df_copy.drop(columns=["lane_id","carrier_id"], inplace=True)
    shipment_df_copy = shipment_df_copy.rename(columns={"shipment_id": "Shipment_Id",
                                     "origin_warehouse": "Origin_Warehouse",
                                     "destination_store": "Destination",
                                     "carrier": "Carrier",
                                     "service": "Service",
                                     "status": "Status",
                                     "ship_date": "Shipment_Date",
                                     "delivery_date": "Delivery_Date",
                                     "weight": "Weight_kg",
                                     "transit_days": "Transit_Days",
                                     "miles": "Distance_Miles",
                                     "cost": "Cost"})

    return shipment_df_copy

def export_shipment_csv(shipment_df):
    """export shipment_dataframe to csv"""
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data_outputs"
    file_name = "logistics_shipment_dataset.csv"
    shipment_df.to_csv(DATA_PATH / file_name, index=False)