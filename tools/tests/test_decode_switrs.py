from tools import decode_switrs
import numpy as np
import pandas as pd


def test_loaddata():

    try:
        # read in data
        crashes = pd.read_csv('../../data/Crashes.csv')
       
    except:
        print("Cannot load data")
        quit()
        
    assert crashes.shape[0] == 5094
    print("...test_loaddata() PASSED")


def test_decode():
    crashes = pd.read_csv('../../data/Crashes.csv')
    df_clean = decode.decode_switrs(crashes, create_new_columns=True)

    
    assert df_clean.shape == (88, 5094)
    print("...test_loaddata() PASSED")

if __name__ == "__main__":
    print("--- Starting Simple Tests ---")
    
    test_loaddata()
    test_decode()
    print("\n--- All Simple Tests Passed! ---")