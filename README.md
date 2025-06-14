# Arithmetic Puzzle Solver

A comprehensive Python implementation for solving KenKen and similar arithmetic puzzles using various constraint satisfaction algorithms.

## Overview

This project implements multiple algorithms to solve arithmetic puzzles (KenKen) of varying sizes. The solver uses constraint satisfaction techniques including AC-3 arc consistency, backtracking with forward checking, and comparison with OR-Tools CP-SAT solver.

## Features

- **Multiple Solving Algorithms**:
  - AC-3 (Arc Consistency Algorithm)
  - AC-3 + Backtracking
  - Backtracking with Forward Checking
  - Pure Backtracking (no forward checking)
  
- **Puzzle Support**:
  - Variable grid sizes (4×4, 6×6, 8×8, 9×9)
  - Arithmetic operations: addition, subtraction, multiplication, division
  - Single-cell constraints
  
- **Performance Analysis**:
  - Benchmarking across different algorithms
  - Statistical analysis with visualization
  - Comparison with OR-Tools solver


## Installation

```bash
# Required dependencies
pip install numpy matplotlib ortools
```

## Usage

### Basic Solving

```python
from arithmetic_puzzle import ArithmeticPuzzleSolver

# Define puzzle: 4×4 KenKen
n = 4
groups = [
    ({(0,0), (0,1), (1,0)}, 'mult', 24),
    ({(0,2), (0,3)}, 'div', 2),
    ({(1,1), (1,2)}, 'sub', 3),
    # ... more groups
]

# Create solver and solve
solver = ArithmeticPuzzleSolver(n, groups)
solution = solver.solve('ac3+backtracking')

if solution:
    # Print solution grid
    for i in range(n):
        row = [str(solution.get((i, j), '.')) for j in range(n)]
        print("|" + "|".join(f" {x} " for x in row) + "|")
```

### Algorithm Options

- `"ac3"`: Arc consistency only
- `"ac3+backtracking"`: AC-3 followed by backtracking
- `"backtracking"`: Standard backtracking with forward checking
- `"backtracking_no_fc"`: Pure backtracking without forward checking

### Performance Benchmarking

```python
from example import run_experiment, plot_results_grouped

# Run 10 trials for each algorithm on multiple puzzles
results, raw_results = run_experiment()

# Generate performance plots
plot_results_grouped(results)
```

## Puzzle Format

Puzzles are defined using:
- `n`: Grid size (n×n)
- `groups`: List of tuples `(cells, operation, target)`
  - `cells`: Set of (row, col) coordinates
  - `operation`: `'add'`, `'sub'`, `'mult'`, `'div'`, or `''` (single cell)
  - `target`: Target value for the operation

Example:
```python
groups = [
    ({(0,0), (0,1)}, 'add', 7),      # Cells (0,0) and (0,1) sum to 7
    ({(1,0)}, '', 3),                # Cell (1,0) equals 3
    ({(0,2), (1,2)}, 'mult', 12),    # Cells (0,2) and (1,2) multiply to 12
]
```

## Algorithms Implemented

### AC-3 (Arc Consistency)
Reduces variable domains by enforcing arc consistency across all constraints before search.

### Backtracking with Forward Checking
- Uses Minimum Remaining Values (MRV) heuristic for variable ordering
- Forward checking eliminates inconsistent values from future variables
- Maintains arc consistency during search

### Constraint Handling
- **Row/Column Uniqueness**: Each number 1-n appears exactly once per row/column
- **Arithmetic Constraints**: Cage operations must equal target values
- **Domain Reduction**: Intelligent pruning of impossible values

## Performance Analysis

The project includes comprehensive benchmarking that measures:
- Best, worst, and average solving times
- Algorithm comparison across puzzle sizes
- Statistical visualization with error bars

## Example Puzzles

The project includes several test puzzles:
- 4×4 puzzle (7 cages)
- 6×6 puzzle (17 cages) 
- 8×8 puzzle (29 cages)
- 9×9 puzzle (35 cages)

## Comparison with OR-Tools

`test.py` provides a reference implementation using Google's OR-Tools CP-SAT solver for validation and performance comparison.

## Mathematical Notation

The solver handles various mathematical operations:
- **Addition**: \( \sum_{i} x_i = \text{target} \)
- **Subtraction**: \( |x_1 - x_2| = \text{target} \)
- **Multiplication**: \( \prod_{i} x_i = \text{target} \)
- **Division**: \( \frac{\max(x_1, x_2)}{\min(x_1, x_2)} = \text{target} \)

## Contributing

Feel free to contribute by:
- Adding new puzzle instances
- Implementing additional CSP algorithms
- Improving performance optimizations
- Enhancing visualization features

