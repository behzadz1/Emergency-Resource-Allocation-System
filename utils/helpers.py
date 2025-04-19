# utils/helpers.py

import re


def calculate_zone_distance(zone1: str, zone2: str) -> int:
    """
    Calculates the simulated distance between two zones.

    Assumes zones are formatted like 'Zone 1', 'Zone 2', etc.

    :param zone1: The first location string.
    :param zone2: The second location string.
    :return: Integer distance (e.g., abs(1 - 3) = 2).
    """
    try:
        z1 = int(_extract_zone_number(zone1))
        z2 = int(_extract_zone_number(zone2))
        return abs(z1 - z2)
    except Exception:
        # Fallback if parsing fails: treat as far apart
        return 99


def _extract_zone_number(zone: str) -> int:
    """
    Extracts the number from a zone string like 'Zone 4'.

    :param zone: String like 'Zone 4'.
    :return: Integer zone number (e.g., 4).
    """
    match = re.search(r'\d+', zone)
    if match:
        return int(match.group())
    raise ValueError(f"Invalid zone format: {zone}")

