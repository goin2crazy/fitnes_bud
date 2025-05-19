import json
import os
import numpy as np 
import pandas as pd 

from utils import load_config 


def sum_count_per_day_dict(df: pd.DataFrame) -> dict:
    """
    Calculates the sum of the 'count' column per day and returns it as a dictionary.

    Assumes the input DataFrame has columns named 'timestamp' and 'count'.

    Args:
        df: A pandas DataFrame with 'timestamp' (datetime or convertible)
            and 'count' (numeric) columns.

    Returns:
        A dictionary where keys are dates (as pandas Timestamps) and
        values are the sum of 'count' for that day.
    """
    # Ensure the 'timestamp' column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Drop rows where timestamp conversion failed
    df.dropna(subset=['timestamp'], inplace=True)

    # Set the timestamp as the index
    df = df.set_index('timestamp')

    # Resample by day ('D') and calculate the sum of the 'count' column
    daily_sum_series = df['count'].resample('D').sum()

    # Convert the pandas Series to a dictionary
    daily_sum_dict = daily_sum_series.to_dict()

    return daily_sum_dict

# --- New function to load activity frequency ---
def load_activity_frequency():
    """
    Simulates loading activity frequency data.
    Returns a list of RGB color tuples.
    Example: [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    response_format = {
        "month_count": [], 
        "min": {"count": 0, "color": (0, 0, 0)}, 
        "max": {"count": 0, "color": (0, 0, 0)}, 
        "average": 0 
    }

    try: 
        config = load_config()
        dataset_path = config['dataset_path']
        
        if dataset_path.endswith("json"): 
            dataset = pd.read_json(dataset_path)
        elif dataset_path.endswith("csv"): 
            dataset = pd.read_csv(dataset_path)
        else: 
            assert ("Dataset is incorrect format")

        last_month_counts = sum_count_per_day_dict(dataset)
        print(last_month_counts)

        last_month_counts = list(last_month_counts.values())[-30:]
        
        max_count = max(last_month_counts)
        last_month_counts_normalized = [i/max_count for i in last_month_counts]

        last_month_counts_to_color = [(int(50+100* i), int(255*i), int(255*i)) for i in last_month_counts_normalized]

        response_format['month_count'] = last_month_counts_to_color

        max_id = np.argmax([sum(i) for i in last_month_counts_to_color])
        response_format['max']['color'] = last_month_counts_to_color[max_id]
        response_format['max']['count'] = last_month_counts[max_id]

        min_id = np.argmin([sum(i) for i in last_month_counts_to_color])
        response_format['min']['color'] = last_month_counts_to_color[min_id]
        response_format['min']['count'] = last_month_counts[min_id]

        average_count = sum(last_month_counts)/len(last_month_counts)
        response_format['average'] = int(average_count)

        return response_format
        
    except Exception as e: 
        print(e)
        response_format['month_count'] = [
            (15, 15, 15),
        ]
        return response_format

