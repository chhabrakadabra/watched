from pkg_resources import DistributionNotFound, get_distribution

from .main import main

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
