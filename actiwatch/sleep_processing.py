"""Sleep and light processing"""

# import pandas as pd
import numpy as np
from .helpers import encode, decode


def windowed_sleep(col, threshold: int, sampling_interval: int):
    """Replicates Actiware's threshold-based sleep-staging algorithm

    Args:
      col (list): Data frame column, as list, which we will be acting on
      threshold (int): Lower bound for levels to be considered "Wake"
      sampling_interval (int): Configured watch sampling frequency.

    Returns:
      A same-length np.array of Sleep and Wake values

    Example:
      windowed_sleep(df['Activity'].tolist(), 40)
    """

    if not sampling_interval in [15, 30, 60, 120]:
        raise ValueError("'sampling_interval' must be on one: 15, 30, 60, or 120")

    temp = [np.nan]

    if sampling_interval == 15:
        y = (
            (col[indx - 8] * (1 / 25))
            + (col[indx - 7] * (1 / 25))
            + (col[indx - 6] * (1 / 25))
            + (col[indx - 5] * (1 / 25))
            + (col[indx - 4] * (1 / 5))
            + (col[indx - 3] * (1 / 5))
            + (col[indx - 2] * (1 / 5))
            + (col[indx - 1] * (1 / 5))
            + (col[indx] * 4)
            + (col[indx + 1] * (1 / 5))
            + (col[indx + 2] * (1 / 5))
            + (col[indx + 3] * (1 / 5))
            + (col[indx + 4] * (1 / 5))
            + (col[indx + 5] * (1 / 25))
            + (col[indx + 6] * (1 / 25))
            + (col[indx + 7] * (1 / 25))
            + (col[indx + 8] * (1 / 25))
        )

        temp.append(y)

    if sampling_interval == 30:
        y = (
            (col[indx - 4] * (1 / 25))
            + (col[indx - 3] * (1 / 25))
            + (col[indx - 2] * (1 / 5))
            + (col[indx - 1] * (1 / 5))
            + (col[indx] * 2)
            + (col[indx + 1] * (1 / 5))
            + (col[indx + 2] * (1 / 5))
            + (col[indx + 3] * (1 / 25))
            + (col[indx + 4] * (1 / 25))
        )
        temp.append(y)

    if sampling_interval == 60:
        for indx in range(1, len(col) - 1):
            y = (
                (col[indx - 2] * (1 / 25))
                + (col[indx - 1] * (1 / 5))
                + (col[indx] * 1)
                + (col[indx + 1] * (1 / 5))
                + (col[indx + 2] * (1 / 25))
            )
            temp.append(y)

    if sampling_interval == 120:
        for indx in range(1, len(col) - 1):
            y = (col[indx - 1] * 0.12) + (col[indx] * 0.5) + (col[indx + 1] * 0.12)
            temp.append(y)

    temp.append(np.nan)
    temp2 = [i > threshold for i in temp]
    output = np.where(temp2, "Wake", "Sleep")
    return output


# def process_sleep(df):
#     """Lotjonen Parameters, Off-Wrist Detection, and Sleep Smoothing

#     This and the following few sections add a ton of variables to our main
#     dataframe. Most relate to various ways to interpret sleep staging, light
#     exposure, and activity, but there are a few notable exceptions, like
#     `Noon_Day`.
#     """
#     df["Lotjonen_mean"] = df["Activity"].rolling(15, center=True).mean()
#     df["Lotjonen_sd"] = df["Activity"].rolling(17, center=True).std()
#     df["Lotjonen_ln"] = np.log(df["Activity"]) + 0.1
#     df["Lotjonen_Counts"] = df["Activity"] > 10

#     df["Sleep_Thresh"] = np.where(df["Lotjonen_mean"] < 100, "Sleep", "Wake")
#     df["Activity_diff"] = df["Activity"].diff()

#     return df


## TODO:
def smooth_sleep(column):
    """Recursively smooth sleep staging

    Args:
        column (list): Data frame column, as list, which we will be acting on

    Returns:
        np.array containing 'Sleep' and 'Wake', same length as 'df_col'

    Example:
        smooth_sleep(df['Sleep_Thresh'].tolist())
    """

    def _rle_to_df(rle_obj):
        """Convert RLE `encode` object to pd.DataFrame

        Example:
            _rle_to_df(encode(df['Sleep_Thresh'].tolist()))
        """
        raise NotImplementedError
        # return pd.DataFrame(rle_obj, columns=["Length", "Value"])

    def _cole_post_process(rle_df):
        old = rle_df.copy()
        rle_df["Shift"] = rle_df["Length"].shift(1)
        # ...

    raise (NotImplementedError)
