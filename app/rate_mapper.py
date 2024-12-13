"""
This module provides utility functions for story video generation.
"""
def get_speech_rate(rate):
    """
    Maps user-friendly rate labels to numeric values.

    Args:
        rate (str): The user-friendly rate label ('slow', 'normal', 'fast').

    Returns:
        int: The numeric value corresponding to the rate.

    Raises:
        ValueError: If the rate is not valid.
    """
    rate_mapping = {
        "slow": 50,
        "normal": 100,
        "fast": 150
    }

    try:
        return rate_mapping[rate]
    except KeyError:
        raise ValueError("Invalid rate. Choose from 'slow', 'normal', or 'fast'.")
