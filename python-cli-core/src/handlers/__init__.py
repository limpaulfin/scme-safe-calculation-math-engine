"""
Operation handlers module - COMPLETE IMPLEMENTATION
"""

from .uuid_handler import handle_uuid
from .random_handler import handle_random
from .eval_handler import handle_eval
from .base_handler import handle_base_convert
from .count_handler import handle_count
from .const_handler import handle_const_get, handle_const_list
from .complex_handler import handle_complex_eval, handle_complex_to_polar, handle_complex_from_polar
from .math_handler import handle_combinatorics, handle_number_theory
from .stats_handler import handle_stats_describe, handle_stats_regress, handle_prob_dist, handle_stat_test
from .solver_handler import handle_solve_linear, handle_solve_poly
from .calculus_handler import handle_differentiate, handle_integrate, handle_limit
from .units_handler import handle_units_convert, handle_units_quick, handle_units_list
from .matrix_handler import handle_matrix_op
from .vector_handler import handle_vector_op
from .batch_handler import handle_batch

__all__ = [
    'handle_uuid', 'handle_random', 'handle_eval', 'handle_base_convert', 'handle_count',
    'handle_const_get', 'handle_const_list', 'handle_complex_eval', 'handle_complex_to_polar',
    'handle_complex_from_polar', 'handle_combinatorics', 'handle_number_theory',
    'handle_stats_describe', 'handle_stats_regress', 'handle_prob_dist', 'handle_stat_test',
    'handle_solve_linear', 'handle_solve_poly', 'handle_differentiate', 'handle_integrate',
    'handle_limit', 'handle_units_convert', 'handle_units_quick', 'handle_units_list',
    'handle_matrix_op', 'handle_vector_op', 'handle_batch'
]
