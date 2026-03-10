import pandas as pd
import pathlib

def _require_columns(df: pd.DataFrame, required: list[str], label:str) -> None:
    """quality check for required columns"""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{label}: missing required columns: {missing}. Found {list(df.columns)}")

def load_carrier_matrix(path:pathlib.Path) -> pd.DataFrame:
    """load carrier name and id into dataframe"""
    df = pd.read_csv(path)
    _require_columns(df, ["carrier_id", "carrier_name"], "carrier_matrix")
    df = df.dropna(subset=["carrier_id", "carrier_name"]).copy()
    df["carrier_id"] = df["carrier_id"].astype(str).str.strip()
    df["carrier_name"] = df["carrier_name"].astype(str).str.strip()

    if df["carrier_id"].duplicated().any():
        dupes = df.loc[df["carrier_id"].duplicated(keep=False), "carrier_id"].unique().tolist()
        raise ValueError(f"carrier_matrix: duplicate carrier_id values: {dupes}")
    return df

def load_lane_id_route(path:pathlib.Path) -> pd.DataFrame:
    """load lane id, origin, destination, and miles into dataframe"""
    df = pd.read_csv(path)
    _require_columns(df, ["lane_id", "origin_warehouse", "destination_store", "miles"], "lane_id_route")
    df = df.dropna(subset=["lane_id", "origin_warehouse", "destination_store", "miles"]).copy()
    df["lane_id"] = df["lane_id"].astype(str).str.strip()
    df["origin_warehouse"] = df["origin_warehouse"].astype(str).str.strip()
    df["destination_store"] = df["destination_store"].astype(str).str.strip()
    df["miles"] = pd.to_numeric(df["miles"], errors="coerce")

    if df["miles"].isna().any():
        bad = df.loc[df["miles"].isna(), ["lane_id"]].head(10)
        raise ValueError(f"lane_id_route: non-numeric miles found (showing up to 10 lane_ids):\n{bad}")

    if df["lane_id"].duplicated().any():
        dupes = df[df["lane_id"].duplicated()]["lane_id"].unique().tolist()[:10]
        raise ValueError(f"lane_id_route: duplicate lane_id values (showing up to 10): {dupes}")
    return df

def load_carrier_route_matrix(path:pathlib.Path) -> pd.DataFrame:
    """load lane id and carrier id into dataframe"""
    df = pd.read_csv(path)
    _require_columns(df, ["lane_id", "carrier_id"], "carrier_route_matrix")
    df = df.dropna(subset=["lane_id", "carrier_id"]).copy()
    df["lane_id"] = df["lane_id"].astype(str).str.strip()
    df["carrier_id"] = df["carrier_id"].astype(str).str.strip()

    dup_mask = df.duplicated(subset=["lane_id", "carrier_id"], keep=False)
    if dup_mask.any():
        dupes = df.loc[dup_mask, ["lane_id", "carrier_id"]].drop_duplicates().head(10)
        raise ValueError(
            "carrier_route_matrix: duplicate (lane_id, carrier_id) pairs found "
            f"(showing up to 10):\n{dupes.to_string(index=False)}"
        )
    return df

def load_pricing(path:pathlib.Path) -> dict:
    """load pricing value into a dict of dataframes based on pricing structure"""
    df = pd.read_csv(path)
    _require_columns(df, ["carrier_id", "price_type", "determinant", "value"], "carrier_pricing")
    df = df.dropna(subset=["carrier_id", "price_type", "determinant", "value"]).copy()
    df["carrier_id"] = df["carrier_id"].astype(str).str.strip()
    df["price_type"] = df["price_type"].astype(str).str.strip()
    df["determinant"] = df["determinant"].astype(str).str.strip()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    if df["value"].isna().any():
        bad = df.loc[df["value"].isna(), ["carrier_id"]].head(10)
        raise ValueError(f"non-numeric value found (showing up to 10 carrier_ids):\n{bad}")

    # split pricing file based on price_type
    allowed_split = {"mile", "weight", "service", "fuel"}
    invalid = set(df["price_type"].unique()) - allowed_split
    if invalid:
        raise ValueError(f"Invalid pricing structure: {invalid}")

    mile_df = df[df["price_type"] == "mile"].copy()
    mile_df["determinant"] = pd.to_numeric(mile_df["determinant"], errors="coerce")
    if mile_df["determinant"].isna().any():
        bad = mile_df.loc[mile_df["determinant"].isna(), ["carrier_id"]].head(10)
        raise ValueError(f"Mile_df - Invalid value in determinant:\n{bad}")
    weight_df = df[df["price_type"] == "weight"].copy()
    weight_df["determinant"] = pd.to_numeric(weight_df["determinant"], errors="coerce")
    if weight_df["determinant"].isna().any():
        bad = weight_df.loc[weight_df["determinant"].isna(), ["carrier_id"]].head(10)
        raise ValueError(f"Weight_df - Invalid value in determinant:\n{bad}")
    service_df = df[df["price_type"] == "service"].copy()
    fuel_df = df[df["price_type"] == "fuel"].copy()

    return {"mile": mile_df, "weight": weight_df, "service": service_df, "fuel": fuel_df}


