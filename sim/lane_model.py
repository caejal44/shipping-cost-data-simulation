import pandas as pd

def build_lane_carrier_df(lane_df: pd.DataFrame, carrier_route_df: pd.DataFrame) -> pd.DataFrame:
    """uses the lane_id to join origin, destination, and miles into a master dataframe"""
    lane_carrier_df = carrier_route_df.merge(lane_df[["lane_id","origin_warehouse", "destination_store", "miles"]],
                                     on="lane_id", how="left")

    # raise error if miles are missing
    if lane_carrier_df["miles"].isna().any():
        raise ValueError("Some lane_id values in carrier_route_matrix.csv were not found in lane_id_route.csv")

    # raise error if duplicated lane_id and carrier_id combination exists
    if lane_carrier_df.duplicated(subset=["lane_id", "carrier_id"]).any():
        dupes = lane_carrier_df.loc[lane_carrier_df.duplicated(subset=["lane_id", "carrier_id"], keep=False),
            ["lane_id", "carrier_id"]].drop_duplicates().head(10)
        raise ValueError(f"Duplicate lane_id, carrier_id in lane_carrier_route: \n"
            f"{dupes.to_string(index=False)}")

    return lane_carrier_df

