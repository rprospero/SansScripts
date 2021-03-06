"""This module creates unified access to all SANS instruments.

The best way of using the module is with a single

    from SansScripting import *
"""


from socket import gethostname
from functools import wraps
from .Instrument import ScanningInstrument
from .Util import user_script  # noqa: F401
from .reduction import sesans_reduction, sesans_connection  # noqa: F401
from .reduction import identify_pairs, sans_reduction  # noqa: F401
from .reduction import sans_connection  # noqa: F401

SCANNING = None


def is_instrument(title):
    """Check if we are running on the instrument with the given name"""
    return title.upper() in gethostname().upper()


if is_instrument("Larmor"):  # pragma: no cover
    from .Larmor import Larmor
    SCANNING = Larmor()
elif is_instrument("Zoom"):  # pragma: no cover
    from .Zoom import Zoom
    SCANNING = Zoom()
else:
    # Default to Larmor if we can't find an instrument
    # This is mostly for development
    from .Larmor import Larmor
    SCANNING = Larmor()


def _local_wrapper(method):
    @wraps(getattr(SCANNING, method))
    def inner(*args, **kwargs):
        """Call the method without the object"""
        return getattr(SCANNING, method)(*args, **kwargs)
    if not inner.__doc__ and hasattr(ScanningInstrument, method):
        inner.__doc__ = getattr(ScanningInstrument, method).__doc__
    return inner


#  Export all of the public methods into the global namespace
for METHOD in dir(SCANNING):
    if METHOD[0] != "_" and METHOD not in locals() and \
       callable(getattr(SCANNING, METHOD)):
        locals()[METHOD] = _local_wrapper(METHOD)
