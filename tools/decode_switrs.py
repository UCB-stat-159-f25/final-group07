import pandas as pd

#SWITRS code documentation: https://tims.berkeley.edu/help/SWITRS.php

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
PC_CODES = {
    'A': 'VC Section Violation',
    'B': 'Other Improper Driving',
    'C': 'Other Than Driver',
    'D': 'Unknown',
    'E': 'Fell Asleep',
    '-': 'Not Stated'
}

PCF_VIOL_CODES = {
    '01': 'Driving or Bicycling Under the Influence of Alcohol or Drug',
    '02': 'Impeding Traffic',
    '03': 'Unsafe Speed',
    '04': 'Following Too Closely',
    '05': 'Wrong Side of Road',
    '06': 'Improper Passing',
    '07': 'Unsafe Lane Change',
    '08': 'Improper Turning',
    '09': 'Automobile Right of Way',
    '10': 'Pedestrian Right of Way',
    '11': 'Pedestrian Violation',
    '12': 'Traffic Signals and Signs',
    '13': 'Hazardous Parking',
    '14': 'Lights',
    '15': 'Brakes',
    '16': 'Other Equipment',
    '17': 'Other Hazardous Violation',
    '18': 'Other Than Driver (or Pedestrian)',
    '19': None, #empty
    '20': None, #empty
    '21': 'Unsafe Starting or Backing',
    '22': 'Other Improper Driving',
    '23': 'Pedestrian or "Other" Under the Influence of Alcohol or Drug',
    '24': 'Fell Asleep',
    '00': 'Unknown',
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
    '1' : 'Monday',
    '2' : 'Tuesday',
    '3' : 'Wednesday',
    '4' : 'Thursday',
    '5' : 'Friday',
    '6' : 'Saturday',
    '7' : 'Sunday'
}




# Map column names to their code dictionary
MASTER_MAP = {
    'WEATHER_1': WEATHER_CODES,
    'WEATHER_2': WEATHER_CODES,
    'COLLISION_SEVERITY': SEVERITY_CODES,
    'TYPE_OF_COLLISION': COLLISION_TYPE_CODES,
    'ROAD_SURFACE': ROAD_SURFACE_CODES,
    'LIGHTING': LIGHTING_CODES,
    'PRIMARY_COLL_FACTOR': PC_CODES,
    'PCF_VIOL_CATEGORY': PCF_VIOL_CODES,
    'DAY_OF_WEEK': DAY_OF_WEEK,
    'MVIW': MOVEMENT_CODES
   
}

def decode_switrs(df):
    """
    Creates new column with decoded inputs from SWITRS codebook

    Parameters: 
      df (DataFrame) : Dataframe with columns that need decoding
      create_new_columns (bool) : Bool on whether to overwrite or create new columns

    Return:
      df (Dataframe) : dataframe with appended decoded columns [{col}'_DESC']
    
    """
    df_decoded = df.copy()
    
    for col, mapping in MASTER_MAP.items():
        if col in df_decoded.columns:
            #non numeric keys
            if col != 'COLLISION_SEVERITY':
                 df_decoded[col] = df_decoded[col].astype(str).str.strip()
            #create columns description
            new_col_name = f"{col}_DESC"
            df_decoded[new_col_name] = df_decoded[col].map(mapping).fillna(df_decoded[col])
            print(f"Created decoded column: {new_col_name}")
           
    return df_decoded