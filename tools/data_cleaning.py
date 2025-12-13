r"""This script defines functions to clean the different SWITRs datasets (separate script is provided for each of Crashes, Victims and Parties).

Usage example (from root diectory):
...
    crashes = clean_crashes("data/Crashes.csv")
    parties = clean_parties("data/Parties.csv")
	victims = clean_victims("data/Victims.csv")
	victim_level = build_victim_level_table("data")
...
"""


import pandas as pd

MISSING_STRINGS = {"-", "- ", " -", "--", ""}


def standardize_object_columns(df: pd.DataFrame):
    """
    Remove random spaces in object columns and convert dash placeholders to NA.
    """
    df = df.copy()
    obj_cols = df.select_dtypes(include="object").columns
    for col in obj_cols:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
        df[col] = df[col].replace(MISSING_STRINGS, pd.NA)
    return df


def _clean_age(series: pd.Series):
    """
    Convert (0, 998) ages to NA.
	This is relevant for the Victims and Parties datasets
    """
    return series.mask(series.isin([0, 998])).astype("Int64")


def clean_crashes(path: str):
    """
    Load and clean crash-level data.

    - Drops constant fields and columns with >95% missingness.
    - Builds collision_datetime/hour from date + HHMM time (invalid >2359 taken to be NA).
    - Uses POINT_X/POINT_Y for coordinates; fills lat/lon from those and
      drops rows still missing location.
    - Converts Y/NA indicators to pandas Boolean.
    """
    df = pd.read_csv(path)
    df = standardize_object_columns(df)
    df = df.drop_duplicates(subset="CASE_ID")

    # Combine lat/long with x/y since at/long have almost all values missing
    df["longitude"] = df["LONGITUDE"].combine_first(df["POINT_X"])
    df["latitude"] = df["LATITUDE"].combine_first(df["POINT_Y"])

    # Remove invalid times and covert to_datetime
    time_col = pd.to_numeric(df["COLLISION_TIME"], errors="coerce")
    time_col = time_col.where((time_col >= 0) & (time_col <= 2359))
    time_str = time_col.astype("Int64").astype(str).str.zfill(4)
    df["collision_datetime"] = pd.to_datetime(
        df["COLLISION_DATE"].astype(str) + " " + time_str,
        format="%Y-%m-%d %H%M",
        errors="coerce",
    )
    df["collision_hour"] = df["collision_datetime"].dt.hour

	# Converts Y/NA indicators to pandas Boolean
    indicator_cols = ["ALCOHOL_INVOLVED", "PEDESTRIAN_ACCIDENT", "MOTORCYCLE_ACCIDENT", "TRUCK_ACCIDENT"]
    for col in indicator_cols:
        if col in df:
            df[col] = df[col].eq("Y").astype("boolean")

    const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    high_na_cols = [c for c in df.columns if df[c].isna().mean() > 0.95]
    drop_cols = set(const_cols + high_na_cols + ["POINT_X", "POINT_Y", "LATITUDE", "LONGITUDE"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
	# Drop rows still missing lat or long (after merging with with x or y)
    df = df[df["latitude"].notna() & df["longitude"].notna()].reset_index(drop=True)

    return df


def clean_parties(path: str):
    """
    Load and clean party-level data.

    - Convert dash placeholders and (0, 998) ages to NA
    - Drops columns with >90% missingness (e.g., CHP_VEH_TYPE_TOWED, INATTENTION).
    - Converts AT_FAULT to Boolean; removes redundant ACCIDENT_YEAR (kept from crashes).
    """
    df = pd.read_csv(path)
    df = standardize_object_columns(df)
    df["PARTY_AGE"] = _clean_age(df["PARTY_AGE"])
    df["PARTY_SEX"] = df["PARTY_SEX"].replace({"X": pd.NA})
    df["AT_FAULT"] = df["AT_FAULT"].map({"Y": True, "N": False}).astype("boolean")

    high_na_cols = [c for c in df.columns if df[c].isna().mean() > 0.90]
    drop_cols = set(high_na_cols + ["ACCIDENT_YEAR"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


def clean_victims(path: str):
    """
    Load and clean victim-level data.

    - Convert dash placeholders and (0, 998) ages to NA
    - Drops constant columns (CITY, COUNTY) since all the data is from San Francisco, and redundant ACCIDENT_YEAR.
    """
    df = pd.read_csv(path)
    df = standardize_object_columns(df)
    df["VICTIM_AGE"] = _clean_age(df["VICTIM_AGE"])
    df["VICTIM_SEX"] = df["VICTIM_SEX"].replace({"X": pd.NA})

    const_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    drop_cols = set(const_cols + ["ACCIDENT_YEAR"])
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


def build_victim_level_table(data_dir: str):
    """
    Victim-level table joined with party and crash context.

    Returns one row per victim with party attributes and crash attributes merged in.
    """
    crashes = clean_crashes("data/Crashes.csv")
    parties = clean_parties("data/Parties.csv")
    victims = clean_victims("data/Victims.csv")

    merged = victims.merge(parties, on=["CASE_ID", "PARTY_NUMBER"], how="left", suffixes=("_victim", "_party"))
    merged = merged.merge(crashes, on="CASE_ID", how="left")
    return merged


