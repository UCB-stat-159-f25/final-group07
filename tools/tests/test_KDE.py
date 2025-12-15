import numpy as np
import pandas as pd
import pytest

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
        If any year is outside the valid range.
    """
    # Convert single int to list for uniformity
    years_to_check = [year] if isinstance(year, int) else list(year)
    
    # Check each year
    for y in years_to_check:
        if y < min_year or y > max_year:
            raise ValueError(f"Invalid year {y}. Must be between {min_year} and {max_year}.")
    
    # If no exception, return True for convenience
    return True

################## TEST ###############################

def test_valid_single_year():
    """Test valid single year within range."""
    assert test_crash_year(2020) is True

def test_valid_list_years():
    """Test valid list of years within range."""
    assert test_crash_year([2018, 2022]) is True

def test_invalid_low_year():
    """Test year below minimum raises ValueError."""
    with pytest.raises(ValueError, match="Invalid year 2010"):
        test_crash_year(2010)

def test_invalid_high_year():
    """Test year above maximum raises ValueError."""
    with pytest.raises(ValueError, match="Invalid year 2025"):
        test_crash_year(2025)

def test_mixed_invalid():
    """Test list with mixed valid/invalid years raises ValueError."""
    with pytest.raises(ValueError, match="Invalid year 2010"):
        test_crash_year([2020, 2010])

def test_boundary_years():
    """Test boundary years (min_year and max_year)."""
    assert test_crash_year(2014) is True
    assert test_crash_year(2024) is True

def test_empty_list():
    """Test empty list returns True."""
    assert test_crash_year([]) is True

def test_custom_range():
    """Test with custom min/max years."""
    assert test_crash_year(2023, min_year=2020, max_year=2025) is True
    with pytest.raises(ValueError, match="Invalid year 2019"):
        test_crash_year(2019, min_year=2020, max_year=2025)

def test_non_integer_input():
    """Test non-integer inputs are handled gracefully."""
    with pytest.raises((ValueError, TypeError)):
        test_crash_year("2020")
    with pytest.raises((ValueError, TypeError)):
        test_crash_year([2020, "2021"])

################# RUN TESTS ###########################################
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
