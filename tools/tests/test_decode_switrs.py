from tools import decode_switrs
import numpy as np
import pandas as pd
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]        # .../final-group07
DATA_PATH = REPO_ROOT / "data" / "Crashes.csv"

def test_loaddata():
    crashes = pd.read_csv(DATA_PATH)
    assert crashes.shape[0] == 5094

def test_decode():
    crashes = pd.read_csv(DATA_PATH)
    df_clean = decode_switrs(crashes, create_new_columns=True)
    assert df_clean.shape == (5094, 90)

    
if __name__ == "__main__":
    print("--- Starting Simple Tests ---")
    
    test_loaddata()
    test_decode()
    print("\n--- All Simple Tests Passed! ---")