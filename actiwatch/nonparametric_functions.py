"""Collection of nonparametric activity functions"""

import random
import numpy as np


def intradaily_variability(data, sample_rate_hz, window_days):
    """Calculate Intradaily Variability for a list of data

    Arguments:
        data (list):
        sample_rate_hz (float):
        window_days (int): Number of days
    """
    raise (NotImplementedError)


def interdaily_stability(activity, sample_rate_hz, window_days):
    """
    Arguments:
        activity (list):
        sample_rate_hz (float):
        window_days (int): Number of days
    """
    ### Samples per hour/day
    sph = int(60 / (1 / sample_rate_hz))
    spd = int(24 * sph)

    ## Reshape array
    rec_days = int(np.ceil(len(activity) / spd))
    activity = np.reshape(activity, (rec_days, spd))
    activity_hourly = np.reshape(activity, (24 * rec_days, sph))

    ## Hourly Mean
    # activity[()]
    raise (NotImplementedError)


sample_rate_hz = 1 / 2
days = 5


def test_iv(sample_rate_hz, days):
    ## Build initial pseudo-sine wave for testing
    ### Samples per day
    spd = int(24 * 60 / (1 / sample_rate_hz))
    sig_len = int(spd * days)

    ### Build signal
    activity = np.array([i / (spd / (2 * np.pi)) for i in range(spd)])
    activity = np.tile(activity, days)
    activity = np.sin(activity)
    activity = np.array([max(0, i + np.random.normal(0, 0.1)) for i in activity])
    activity *= random.randint(0, 1000)
