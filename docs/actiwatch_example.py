# -*- coding: utf-8 -*-

"""
actiwatch example
~~~~~~~~~~~~~~~~~

Example script illustrating how to use the package
"""

from pathlib import PurePath
import glob
import actiwatch
import pandas as pd


def list_files(path: str, mask: str):
    """Generate list of actiwatch files

    Args:
        path (str): Path to containing folder
        mask (str): Regular expression filter

    Example:
        >>> path = "D:/data/acquired_data/human/h4085/Actigraphy/CSV"
        >>> mask = "*_Bedtime.csv"
        >>> list_files(path, mask)
    """
    p = PurePath(path)
    path_str = str(p / mask)
    return glob.glob(path_str)


def map_watch_class(file_paths, start_hour, sleep_threshold, manually_scored):
    """Map actiwatch.Actiwatch class on to a list of actiwatch files

    Args:
        file_paths (list): List of paths to actiwatch data
        start_hour (int): Hour (0-23) that days are split on.
        sleep_threshold (int): Activity threshold for wake scoring (20 = low, 40 = medium, 80 = high).
        manually_scored (bool): Is the file of the 'Bedtime' variety?

    Returns:
        list: List of actiwatch.Actiwatch instances
    """
    return list(
        map(
            lambda x: actiwatch.Actiwatch(
                x,
                start_hour=start_hour,
                sleep_threshold=sleep_threshold,
                manually_scored=manually_scored,
            ),
            file_paths,
        )
    )


def generate_single_result(analysis, watch_list):
    """Returns a dataframe of a single analysis for all instances in 'watch_list'

    Args:
        analysis (str): Analysis property of actiwatch.Actiwatch class
        watch_list (list): List of actiwatch.Actiwatch instances
    """
    if analysis not in actiwatch.Actiwatch.__dict__.keys():
        raise AttributeError(f"Actiwatch class does not have attribute {analysis}")

    if not all([type(i) == actiwatch.Actiwatch for i in watch_list]):
        TypeError("All items in `watch_list` must be instances of <Actiwatch>")

    output_df = pd.DataFrame()

    for watch in watch_list:
        try:
            relevant_data = getattr(watch, analysis)
            output_df = output_df.append(relevant_data, ignore_index=True, sort=True)
        except:
            pass

    return output_df


def generate_all_results(watch_list):
    """Returns a dataframe of all analyses for all instances in 'watch_list'

    Args:
        watch_list (list): List of actiwatch.Actiwatch instances
    """
    analyses = [
        "sleep_metrics",
        "sleep_latency",
        "bedtime",
        "relative_amplitude",
        "total_values",
    ]

    output_df = pd.DataFrame()

    for analysis in analyses:
        analysis_df = generate_single_result(analysis, watch_list)

        if output_df.empty:
            output_df = output_df.append(analysis_df, ignore_index=True, sort=True)
        else:
            output_df = output_df.merge(
                analysis_df, how="outer", on=["watch_ID", "Split_Day"]
            )

    return output_df


def main():
    """Main script function
    """
    path = "D:/data/acquired_data/human/h4085/Actigraphy/CSV"
    acti_files = list_files(path, "*_Bedtime.csv")
    watches = map_watch_class(acti_files[:3], 16, 40, True)

    single_result = generate_single_result(analysis="total_values", watch_list=watches)

    all_results = generate_all_results(watch_list=watches)
    all_results.to_csv("2018-12-20_actigraphy-data.csv")


if __name__ == "__main__":
    main()
