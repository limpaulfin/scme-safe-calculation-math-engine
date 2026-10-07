"""Statistics module"""
from .descriptive import describe_stats
from .regression import regress
from .distributions import prob_dist
from .tests import stat_test
__all__ = ['describe_stats', 'regress', 'prob_dist', 'stat_test']
