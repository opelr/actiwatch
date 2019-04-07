"""Sleep and light processing"""

import numpy as np
from .helpers import encode, decode


def windowed_sleep(col, threshold: int, sampling_interval: int):
    """Replicates Actiware's threshold-based sleep-staging algorithm

    Args:
      col (list): Data frame column, as list, which we will be acting on.
      threshold (int): Lower bound for levels to be considered "Wake"
      sampling_interval (int): Configured watch sampling frequency.

    Returns:
      A same-length np.array of Sleep and Wake values

    Example:
      windowed_sleep(df['Activity'].tolist(), 40)
    """

    if sampling_interval not in [15, 30, 60, 120]:
        raise ValueError("'sampling_interval' must be on one: 15, 30, 60, or 120")

    temp = []

    if sampling_interval == 15:
        for indx in range(len(col)):
            if indx < 8 or indx >= (len(col) - 8):
                temp.append(np.nan)
            else:
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
        for indx in range(len(col)):
            if indx < 4 or indx >= (len(col) - 4):
                temp.append(np.nan)
            else:
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
        for indx in range(len(col)):
            if indx < 2 or indx >= (len(col) - 2):
                temp.append(np.nan)
            else:
                y = (
                    (col[indx - 2] * (1 / 25))
                    + (col[indx - 1] * (1 / 5))
                    + (col[indx] * 1)
                    + (col[indx + 1] * (1 / 5))
                    + (col[indx + 2] * (1 / 25))
                )
                temp.append(y)

    if sampling_interval == 120:
        for indx in range(len(col)):
            if indx < 1 or indx >= (len(col) - 1):
                temp.append(np.nan)
            else:
                y = (col[indx - 1] * 0.12) + (col[indx] * 0.5) + (col[indx + 1] * 0.12)
                temp.append(y)

    temp2 = [i > threshold for i in temp]
    return list(np.where(temp2, "Wake", "Sleep"))


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


def cole_post_process(rle: list, rec_freq: int):
    """Recursively apply sleep smoothing to RLE object

    Args:
        rle_df (list): [description]
        rec_freq (int): [description]
    """
    new = []

    for indx, rle_i in enumerate(rle):
        rle_len, rle_value = rle_i

        if indx == 0 or rle_value is np.nan:
            new.append([rle_len, rle_value])
            continue

        if rle_value == "Wake":
            if rle_len in [1, 2]:
                new.append([rle_len, "Sleep"])
            else:
                new.append([rle_len, rle_value])
            continue

        time_min = (rle_len * rec_freq) // 60
        time_prev_min = (rle[indx - 1][0] * rec_freq) // 60
        try:
            time_post_min = (rle[indx + 1][0] * rec_freq) // 60
        except IndexError:
            time_post_min = 0

        if (
            (time_min == 1 and time_prev_min >= 4)
            or (time_min == 3 and time_prev_min >= 10)
            or (time_min == 4 and time_prev_min >= 15)
            or (time_min == 6 and time_prev_min >= 10 and time_post_min >= 10)
            or (time_min == 10 and time_prev_min >= 20 and time_post_min >= 20)
        ):
            new.append([rle_len, "Wake"])
        else:
            new.append([rle_len, rle_value])

    if rle == new:
        return new
    else:
        recode = encode(decode(new))
        return cole_post_process(recode, rec_freq)


def smooth_sleep(column: list, rec_freq: int):
    """Recursively smooth sleep staging

    Args:
        column (list): Data frame column, as list, which we will be acting on
        rec_freq(int)

    Returns:
        np.array containing 'Sleep' and 'Wake', same length as 'df_col'

    Example:
        smooth_sleep(df['Sleep_Thresh'].tolist())
    """

    rle = encode(column)
    out = cole_post_process(rle, rec_freq)
    return decode(out)
