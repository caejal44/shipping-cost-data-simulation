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

    new_order = ["shipment_id", "carrier", "origin_warehouse", "destination_store", "ship_date", "delivery_date", "status",
                 "weight", "cost", "miles", "transit_days", "lane_id", "carrier_id"]
    shipment_df_copy = shipment_df_copy[new_order]
    shipment_df_copy.drop(columns=["lane_id","carrier_id"], inplace=True)
    return shipment_df_copy

def export_shipment_csv(shipment_df):
    """export shipment_dataframe to csv"""
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data_outputs"
    file_name = "logistics_shipment_dataset.csv"
    shipment_df.to_csv(DATA_PATH / file_name, index=False)