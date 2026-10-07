"""Equation solvers module"""
from .linear import solve_linear_system
from .polynomial import solve_polynomial
__all__ = ['solve_linear_system', 'solve_polynomial']
