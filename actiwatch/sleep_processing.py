"""Sleep and light processing"""

# import pandas as pd
import numpy as np
from .rle import encode, decode

def windowed_sleep(df_col, threshold: int):
    """Replicates Actiware's threshold-based sleep-staging algorithm

    Args:
      df_col (list): Data frame column, as list, which we will be acting on
      threshold (int): Lower bound for levels to be considered "Wake"

    Returns:
      A same-length np.array of Sleep and Wake values

    Example:
      windowed_sleep(df['Activity'].tolist(), 40)
    """

    temp = [np.nan]
    for indx in range(1, len(df_col) - 1):
        y = (df_col[indx - 1] * 0.12) + (df_col[indx] * 0.5) + (df_col[indx + 1] * 0.12)
        temp.append(y)

    temp.append(np.nan)
    temp2 = [i > threshold for i in temp]
    output = np.where(temp2, "Wake", "Sleep")
    return output


def process_sleep(df):
    """Lotjonen Parameters, Off-Wrist Detection, and Sleep Smoothing

    This and the following few sections add a ton of variables to our main
    dataframe. Most relate to various ways to interpret sleep staging, light
    exposure, and activity, but there are a few notable exceptions, like
    `Noon_Day`.
    """
    df["Lotjonen_mean"] = df["Activity"].rolling(15, center=True).mean()
    df["Lotjonen_sd"] = df["Activity"].rolling(17, center=True).std()
    df["Lotjonen_ln"] = np.log(df["Activity"]) + 0.1
    df["Lotjonen_Counts"] = df["Activity"] > 10

    df["Sleep_Thresh"] = np.where(df["Lotjonen_mean"] < 100, "Sleep", "Wake")
    df["Activity_diff"] = df["Activity"].diff()

    return df

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
        return pd.DataFrame(rle_obj, columns=["Length", "Value"])

    def _cole_post_process(rle_df):
        old = rle_df.copy()
        rle_df["Shift"] = rle_df["Length"].shift(1)
        # ...

    raise(NotImplementedError)