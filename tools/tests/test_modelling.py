import numpy as np
import pandas as pd
from tools.data_cleaning import clean_crashes

FEATURE_COLS = [
    "ACCIDENT_YEAR", "COLLISION_TIME", "REPORTING_DISTRICT",
    "PRIMARY_RD", "SECONDARY_RD", "INTERSECTION",
    "WEATHER_1", "PRIMARY_COLL_FACTOR", "HIT_AND_RUN",
    "TYPE_OF_COLLISION", "MVIW", "ROAD_SURFACE", "ROAD_COND_1", "LIGHTING",
    "PEDESTRIAN_ACCIDENT", "MOTORCYCLE_ACCIDENT", "TRUCK_ACCIDENT",
    "ALCOHOL_INVOLVED", "STWD_VEHTYPE_AT_FAULT", "CHP_VEHTYPE_AT_FAULT",
]

def make_target(crashes: pd.DataFrame) -> pd.Series:
    severity_to_group = {1: "KSI", 2: "KSI", 3: "Other injury", 4: "Other injury"}
    return crashes["COLLISION_SEVERITY"].map(severity_to_group).eq("KSI").astype(int)

def test_target_is_binary_and_nontrivial():
    crashes = clean_crashes("data/Crashes.csv")
    y = make_target(crashes)
    assert y.nunique() == 2, "Target not binary"
    ksi_share = y.mean()
    assert 0 < ksi_share < 1, f"KSI share out of bounds: {ksi_share:.3f}"

def test_feature_columns_exist_and_not_all_null():
    crashes = clean_crashes("data/Crashes.csv")
    missing = [c for c in FEATURE_COLS if c not in crashes.columns]
    assert not missing, f"Missing expected columns: {missing}"
    all_null = [c for c in FEATURE_COLS if crashes[c].isna().all()]
    assert not all_null, f"Columns with all null values: {all_null}"
