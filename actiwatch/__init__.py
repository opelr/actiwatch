"""
Actiwatch Module
~~~~~~~~~~~~~~~~

Actiwatch is a Python module built for interacting with Philips Actiwatch actigraphy devices. Basic useage:

    >>> import actiwatch
    >>> watch = actiwatch.Actiwatch("/path/to/file.../watch.csv")
"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

from actiwatch.watch import Actiwatch
import actiwatch.analysis


__all__ = ["Actiwatch"]
