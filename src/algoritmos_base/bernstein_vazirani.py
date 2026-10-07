"""Bernstein-Vazirani: descobrir s em f(x) = s · x (mod 2)."""

from qiskit import QuantumCircuit

from .circuitos import compile_circuit, measure_once


def bv_query(s: str) -> QuantumCircuit:
    """Oráculo de f(x) = s · x (mod 2)."""
    # Um qubit para cada entrada + 1 de saída
    qc = QuantumCircuit(len(s) + 1)

    # Para cada bit de s em ordem reversa (padronização Qiskit), se o bit for 1
    # faz o CNOT do qubit correspondente com o último qubit.
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
    return qc


def bv_algorithm(function: QuantumCircuit) -> str:
    """Devolve s com uma única execução.

    O oráculo seria fornecido "de fora": o algoritmo computa s sem conhecê-la.
    """
    return measure_once(compile_circuit(function))
