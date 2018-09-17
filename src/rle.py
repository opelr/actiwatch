"""Run Length Encoding Functions"""

from itertools import groupby
from typing import Iterable


def encode(sequence: Iterable):
    """Enumerate continuous observations in a sequence

    Args:
        sequence (Iterable): Sequence to enumerate
    """
    return [[len(list(g)), k] for k, g in groupby(sequence)]


def decode(encode_obj: list):
    """Reconstruct `encoded` sequence

    Args:
        encode_obj (list): Encode object (from `encode`) to stitch together
    """
    nested = [[c] * n for n, c in encode_obj]
    return [i for j in nested for i in j]
