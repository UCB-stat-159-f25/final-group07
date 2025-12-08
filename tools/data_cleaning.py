from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
MISSING_STRINGS = {"-", "- ", " -", "--", ""}


def _standardize_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip whitespace in object columns and mark dash-style placeholders as NA.
    """
    df = df.copy()
    obj_cols = df.select_dtypes(include="object").columns
    for col in obj_cols:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
        df[col] = df[col].replace(MISSING_STRINGS, pd.NA)
    return df


def _clean_age(series: pd.Series) -> pd.Series:
    """
    Convert SWITRS age sentinels (0, 998) to NA and keep these as nullable integers.
	This is relevant for the Victims and Parties datasets
    """
    return series.mask(series.isin([0, 998])).astype("Int64")


def clean_crashes(
    path: str | Path = DATA_DIR / "Crashes.csv",
    drop_missing_location: bool = True,
) -> pd.DataFrame:
    """
    Load and clean crash-level data.

    - Drops constant fields and columns with >95% missingness.
    - Builds collision_datetime/hour from date + HHMM time (invalid >2359 -> NA).
    - Uses POINT_X/POINT_Y for coordinates; fills lat/lon from those and optionally
      drops rows still missing location.
    - Converts Y/NA indicators to pandas Boolean.
    """
    df = pd.read_csv(path)
    df = _standardize_object_columns(df)
    df = df.drop_duplicates(subset="CASE_ID")

    # Coordinates: POINT_X/Y are mostly populated; LAT/LONG are almost all NA.
    df["longitude"] = df["LONGITUDE"].combine_first(df["POINT_X"])
    df["latitude"] = df["LATITUDE"].combine_first(df["POINT_Y"])

    # Time handling (6 values > 2359 in raw -> mark NA).
    time_col = pd.to_numeric(df["COLLISION_TIME"], errors="coerce")
    time_col = time_col.where((time_col >= 0) & (time_col <= 2359))
    time_str = time_col.astype("Int64").astype(str).str.zfill(4)
    df["collision_datetime"] = pd.to_datetime(
        df["COLLISION_DATE"].astype(str) + " " + time_str,
        format="%Y-%m-%d %H%M",
        errors="coerce",
    )
    df["collision_hour"] = df["collision_datetime"].dt.hour

    indicator_cols = ["ALCOHOL_INVOLVED", "PEDESTRIAN_ACCIDENT", "MOTORCYCLE_ACCIDENT", "TRUCK_ACCIDENT"]
    for col in indicator_cols:
        if col in df:
            df[col] = df[col].eq("Y").astype("boolean")

    const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    high_na_cols = [c for c in df.columns if df[c].isna().mean() > 0.95]
    drop_cols = set(const_cols + high_na_cols + ["POINT_X", "POINT_Y", "LATITUDE", "LONGITUDE"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    if drop_missing_location:
        df = df[df["latitude"].notna() & df["longitude"].notna()].reset_index(drop=True)

    return df


def clean_parties(path: str | Path = DATA_DIR / "Parties.csv") -> pd.DataFrame:
    """
    Load and clean party-level data.

    - Strips dash placeholders, fixes ages coded as 0/998 -> NA.
    - Drops columns with >90% missingness (e.g., CHP_VEH_TYPE_TOWED, INATTENTION).
    - Converts AT_FAULT to Boolean; removes redundant ACCIDENT_YEAR (kept from crashes).
    """
    df = pd.read_csv(path)
    df = _standardize_object_columns(df)
    df["PARTY_AGE"] = _clean_age(df["PARTY_AGE"])
    df["PARTY_SEX"] = df["PARTY_SEX"].replace({"X": pd.NA})
    df["AT_FAULT"] = df["AT_FAULT"].map({"Y": True, "N": False}).astype("boolean")

    high_na_cols = [c for c in df.columns if df[c].isna().mean() > 0.90]
    drop_cols = set(high_na_cols + ["ACCIDENT_YEAR"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


def clean_victims(path: str | Path = DATA_DIR / "Victims.csv") -> pd.DataFrame:
    """
    Load and clean victim-level data.

    - Strips dash placeholders, fixes ages coded as 0/998 -> NA.
    - Drops constant columns (CITY, COUNTY) since all the data is from San Francisco, and redundant ACCIDENT_YEAR.
    """
    df = pd.read_csv(path)
    df = _standardize_object_columns(df)
    df["VICTIM_AGE"] = _clean_age(df["VICTIM_AGE"])
    df["VICTIM_SEX"] = df["VICTIM_SEX"].replace({"X": pd.NA})

    const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    drop_cols = set(const_cols + ["ACCIDENT_YEAR"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


def build_victim_level_table(
    data_dir: str | Path = DATA_DIR,
    drop_missing_location: bool = True,
) -> pd.DataFrame:
    """
    Victim-level table joined with party and crash context.

    Returns one row per victim with party attributes and crash attributes merged in.
    """
    crashes = clean_crashes(Path(data_dir) / "Crashes.csv", drop_missing_location=drop_missing_location)
    parties = clean_parties(Path(data_dir) / "Parties.csv")
    victims = clean_victims(Path(data_dir) / "Victims.csv")

    merged = victims.merge(parties, on=["CASE_ID", "PARTY_NUMBER"], how="left", suffixes=("_victim", "_party"))
    merged = merged.merge(crashes, on="CASE_ID", how="left")
    return merged


def load_all_clean(data_dir: str | Path = DATA_DIR) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Convenience loader returning (crashes, parties, victims, victim_level_table).
    """
    crashes = clean_crashes(Path(data_dir) / "Crashes.csv")
    parties = clean_parties(Path(data_dir) / "Parties.csv")
    victims = clean_victims(Path(data_dir) / "Victims.csv")
    victim_level = build_victim_level_table(data_dir, drop_missing_location=True)
    return crashes, parties, victims, victim_level


if __name__ == "__main__":
    crashes_df, parties_df, victims_df, merged_df = load_all_clean()
    print("crashes:", crashes_df.shape, "parties:", parties_df.shape, "victims:", victims_df.shape, "merged:", merged_df.shape)
