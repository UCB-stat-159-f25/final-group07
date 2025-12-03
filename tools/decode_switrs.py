import pandas as pd

# --- SWITRS CODEBOOKS ---
# Based on California SWITRS documentation

# A - Weather
WEATHER_CODES = {
    'A': 'Clear',
    'B': 'Cloudy',
    'C': 'Raining',
    'D': 'Snowing',
    'E': 'Fog',
    'F': 'Other',
    'G': 'Wind',
    '-': 'Not Stated'
}

# Collision Severity
SEVERITY_CODES = {
    1: 'Fatal',
    2: 'Injury (Severe)',
    3: 'Injury (Other Visible)',
    4: 'Injury (Complaint of Pain)',
    0: 'Property Damage Only'
}

# Type of Collision
COLLISION_TYPE_CODES = {
    'A': 'Head-On',
    'B': 'Sideswipe',
    'C': 'Rear End',
    'D': 'Broadside',
    'E': 'Hit Object',
    'F': 'Overturned',
    'G': 'Vehicle/Pedestrian',
    'H': 'Other',
    '-': 'Not Stated'
}

# Road Surface
ROAD_SURFACE_CODES = {
    'A': 'Dry',
    'B': 'Wet',
    'C': 'Snowy',
    'D': 'Icy',
    'E': 'Slippery (Mud/Oil)',
    'F': 'Loose Material',
    'G': 'Rough',
    'H': 'Damaged',
    'I': 'Construction',
    'J': 'Other',
    '-': 'Not Stated'
}

# Lighting
LIGHTING_CODES = {
    'A': 'Daylight',
    'B': 'Dusk - Dawn',
    'C': 'Dark - Street Lights',
    'D': 'Dark - No Street Lights',
    'E': 'Dark - Street Lights Not Functioning',
    '-': 'Not Stated'
}

# Primary Collision Factor (PCF)
PCF_CODES = {
    'A': 'VC Section Violation',
    'B': 'Other Improper Driving',
    'C': 'Other Than Driver',
    'D': 'Unknown',
    'E': 'Fell Asleep',
    '-': 'Not Stated'
}

# Movement Preceding Collision
MOVEMENT_CODES = {
    'A': 'Stopped',
    'B': 'Proceeding Straight',
    'C': 'Ran Red Light',
    'D': 'Ran Stop Sign',
    'E': 'U-Turn',
    'F': 'Left Turn',
    'G': 'Right Turn',
    'H': 'Slowing/Stopping',
    'J': 'Changing Lanes',
    'K': 'Parking Maneuver',
    'L': 'Entering Traffic',
    'M': 'Other Unsafe Turning',
    'N': 'Xing into Opposing Lane',
    'O': 'Parked',
    'P': 'Merging',
    'Q': 'Traveling Wrong Way',
    'R': 'Other',
    '-': 'Not Stated'
}
DAY_OF_WEEK = {
    '1' : 'Monday'
    '2' : 'Tuesday'
    '3' : 'Wednesday'
    '4' : 'Thursday'
    '5' : 'Friday'
    '6' : 'Saturday'
    '7' : 'Sunday'
}

# Master dictionary mapping column names to their codebook
# You can add more columns here as you define them
MASTER_MAP = {
    'WEATHER_1': WEATHER_CODES,
    'WEATHER_2': WEATHER_CODES,
    'COLLISION_SEVERITY': SEVERITY_CODES,
    'TYPE_OF_COLLISION': COLLISION_TYPE_CODES,
    'ROAD_SURFACE': ROAD_SURFACE_CODES,
    'LIGHTING': LIGHTING_CODES,
    'PCF_VIOL_CATEGORY': PCF_CODES,
    'DAY_OF_WEEK': DAY_OF_WEEK,
    'MVIW': MOVEMENT_CODES  
}

def decode_switrs(df, create_new_columns=True):
    """
    explain here
    """
    df_decoded = df.copy()
    
    for col, mapping in MASTER_MAP.items():
        if col in df_decoded.columns:
            #numeric codes
            if col != 'COLLISION_SEVERITY':
                 df_decoded[col] = df_decoded[col].astype(str).str.strip()

            if create_new_columns:
                new_col_name = f"{col}_DESC"
                # Map the values, filling unknown ones with the original value or 'Unknown'
                df_decoded[new_col_name] = df_decoded[col].map(mapping).fillna(df_decoded[col])
                print(f"Created decoded column: {new_col_name}")
            else:
                df_decoded[col] = df_decoded[col].map(mapping).fillna(df_decoded[col])
                print(f"Overwrote column with descriptions: {col}")
                
    return df_decoded