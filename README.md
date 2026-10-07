# Algoritmos de consulta em Qiskit

Código exploratório. Implementações de **Deutsch**, **Deutsch-Jozsa**, **Bernstein-Vazirani** e **Simon**, feitas acompanhando o IBM Quantum Learning e a disciplina de Computação Quântica (UFMG, 2026/1).

Todos seguem o mesmo esqueleto: **H → oráculo → H → medição**.

| Algoritmo | Pergunta | Execuções | Ideia |
|---|---|---|---|
| Deutsch | f: {0,1}→{0,1} é constante ou balanceada? | 1 | phase kickback com a saída em \|−⟩ |
| Deutsch-Jozsa | idem, para n bits | 1 | medir 0…0 ⇔ constante |
| Bernstein-Vazirani | qual é s em f(x) = s·x mod 2? | 1 | cada bit 1 de s vira uma fase |
| Simon | qual é s em f(x) = f(x⊕s)? | ~n−1 + pós-processamento | cada y medido satisfaz y·s = 0 mod 2 |

## Estrutura

```
.
├── src/algoritmos_consulta/
│   ├── circuitos.py            # compile_circuit (phase kickback), sample, measure_once
│   ├── deutsch.py              # deutsch_function, dj_query, run_algorithm
│   ├── bernstein_vazirani.py   # bv_query, bv_algorithm
│   └── simon.py                # simon_query, simon_circuit, dot_mod2, find_s, simon_algorithm
├── notebooks/demo.ipynb        # uso dos módulos, com circuitos e histogramas
└── pyproject.toml
```

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
jupyter lab notebooks/demo.ipynb
```

## Uso

```python
from algoritmos_consulta import *

run_algorithm(deutsch_function(2))   # 'balanced'
run_algorithm(dj_query(3))           # 'constant' ou 'balanced'
bv_algorithm(bv_query("1011"))       # '1011'
simon_algorithm(simon_query("101"))  # ['101']
```

## Notas

- **Little-endian (Qiskit):** o qubit 0 é o caractere mais à direita de uma string de bits. Por isso os oráculos usam `reversed(s)`. As strings medidas e os candidatos de `find_s` estão na mesma convenção, então lá não é preciso inverter.
- **Oráculo do Simon:** a camada 1 copia `x` para a saída. A camada 2 escolhe um `i` com `sᵢ = 1` e, se `xᵢ = 1`, faz XOR de `s` inteiro na saída. Todos os CNOTs dessa camada têm **o mesmo controle** `i`.
- **`find_s`** devolve todos os candidatos. Uma lista com mais de um elemento significa que faltam medidas independentes.
