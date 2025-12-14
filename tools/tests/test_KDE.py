from tools import KDE
import numpy as np
import pandas as pd

def test_crash_year(year, min_year=2014, max_year=2024):
    """
    Validates that a given year or list of years is within a valid range.

    Parameters
    ----------
    year : int or list of ints
        Year or list of years to validate.
    min_year : int, optional
        Minimum allowed year (default 2014).
    max_year : int, optional
        Maximum allowed year (default 2024).

    Raises
    ------
    ValueError
        HEY! The year variable is outside the valid range (2014-2024).
    """
    # Convert single int to list for uniformity
    years_to_check = [year] if isinstance(year, int) else list(year)
    
    # Check each year
    for y in years_to_check:
        if y < min_year or y > max_year:
            raise ValueError(f"Invalid year {y}. Must be between {min_year} and {max_year}.")
    
    # If no exception, return True for convenience
    return True

