import os


def datapath(*args):
    """Provides explicit path to data directory.

    Args:
        args: As many strings as wanted to get to file.
        For example, datapath("equity", "VSLR.csv") returns
        absolute path to data/equity/VSLR.csv.
    Returns:
        Absolute path to file in data directory.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    data_directory = os.path.join(here, "data")
    return os.path.join(data_directory, *args)
