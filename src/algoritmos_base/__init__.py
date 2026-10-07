"""Algoritmos de consulta em Qiskit: Deutsch, Deutsch-Jozsa, Bernstein-Vazirani e Simon."""

from .bernstein_vazirani import bv_algorithm, bv_query
from .circuitos import compile_circuit, measure_once, sample
from .deutsch import deutsch_function, dj_query, run_algorithm
from .simon import dot_mod2, find_s, simon_algorithm, simon_circuit, simon_query
