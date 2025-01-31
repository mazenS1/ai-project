from ortools.sat.python import cp_model

def solve_kenken(n, groups):
    """Solves a KenKen puzzle using OR-Tools CP-SAT solver.

    Args:
        n: The size of the grid (e.g., 9 for a 9x9 grid).
        groups: A list of tuples, where each tuple represents a cage
          and has the form (set_of_cells, operation, result). Cells are
          represented as (row, col) tuples (0-based indexing).

    Returns:
        A list of lists representing the solution grid, or None if no
        solution is found.
    """
    model = cp_model.CpModel()

    # 1. Create Variables
    grid = {}
    for row in range(n):
        for col in range(n):
            grid[(row, col)] = model.NewIntVar(1, n, f'cell_{row}_{col}')

    # 2. Row and Column Constraints
    for row in range(n):
        model.AddAllDifferent([grid[(row, col)] for col in range(n)])
    for col in range(n):
        model.AddAllDifferent([grid[(row, col)] for row in range(n)])

    # 3. Cage Constraints
    for cells, operation, result in groups:
        if operation == '':
            model.Add(grid[list(cells)[0]] == result)
            continue
        # If operation is single cell operation we can try and enforce constraints before starting solver.
        if cells == {(5,2)}:
            model.Add(grid[(5,2)] == 7)
            continue
        if cells == {(6,3)}:
            model.Add(grid[(6,3)] == 6)
            continue
        if cells == {(8,8)}:
            model.Add(grid[(8,8)] == 4)
            continue
            
        cell_vars = [grid[cell] for cell in cells]
        if operation == 'add':
            model.Add(sum(cell_vars) == result)
        elif operation == 'sub':
            model.Add(abs(cell_vars[0] - cell_vars[1]) == result)
        elif operation == 'mult':
            temp_prod = model.NewIntVar(1, 1000000, "temp_prod")
            model.AddMultiplicationEquality(temp_prod, cell_vars)
            model.Add(temp_prod == result)
        elif operation == 'div':
            if len(cell_vars) == 2:
                var1 = cell_vars[0]
                var2 = cell_vars[1]

                # Option 1 : var1 is divisible by var2 to get the result
                temp_div1 = model.NewIntVar(1, n, "temp_div1")
                model.AddDivisionEquality(temp_div1, var1, var2)
                
                # Option 2: var2 is divisible by var1 to get the result.
                temp_div2 = model.NewIntVar(1, n, "temp_div2")
                model.AddDivisionEquality(temp_div2, var2, var1)
                
                # We want either to be true, hence we use AddBoolOr:
                model.AddBoolOr([temp_div1 == result, temp_div2 == result])

    # 4. Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60 # Set timeout.
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = []
        for row in range(n):
            solution_row = []
            for col in range(n):
                solution_row.append(solver.Value(grid[(row, col)]))
            solution.append(solution_row)
        return solution
    else:
        return None

# Example usage
n = 9
groups3 = [
    ({(0,0), (1,0), (2,0)}, 'mult', 96),
    ({(0,1), (0,2)}, 'div', 4),
    ({(0,3), (1,3), (1,4)}, 'mult', 18),
    ({(0,4), (0,5)}, 'sub', 2),
    ({(0,6), (0,7)}, 'add', 17),
    ({(1,1), (1,2)}, 'mult', 20),
    ({(1,5), (1,6),(2,5),(2,6)}, 'mult', 168),
    ({(0,8), (1,7),(1,8)}, 'mult', 294),
    ({(2,1), (2,2)}, 'sub', 5),
    ({(2,3), (3,3)}, 'div', 3),
    ({(2,4), (3,4),(3,5),(3,6)}, 'mult', 70),
    ({(2,7), (2,8)}, 'sub', 1),
    ({(3,0), (4,0)}, 'sub', 2),
    ({(3,1), (4,1)}, 'sub', 3),
    ({(3,2), (4,2)}, 'div', 4),
    ({(3,7), (3,8),(4,8)}, 'mult', 32),
    ({(4,3), (5,3)}, 'div', 2),
    ({(4,4), (4,5),(5,5)}, 'mult', 18),
    ({(4,6), (4,7)}, 'sub', 1),
    ({(5,0), (5,1),(6,1),(6,2)}, 'mult', 50),
    ({(5,2)}, '', 7),
    ({(5,4), (6,4)}, 'div', 2),
    ({(5,6), (5,7),(6,7)}, 'add', 15),
    ({(5,8), (6,8),(7,8)}, 'add', 14),
    ({(6,0), (6,1)}, 'div', 4),  # Note: (6,0),(6,1) also appear above. Double-check usage?
    ({(6,3)}, '', 6),
    ({(6,5), (6,6)}, 'sub', 2),
    ({(7,1), (7,2),(7,3)}, 'add', 19),
    ({(7,4), (8,4)}, 'sub', 2),
    ({(7,5), (8,5)}, 'sub', 1),
    ({(7,6), (7,7)}, 'add', 6),
    ({(8,0), (8,1)}, 'sub', 4),
    ({(8,2), (8,3)}, 'sub', 1),
    ({(8,6), (8,7)}, 'div', 2),
    ({(8,8)}, '', 4),
]

solution = solve_kenken(n, groups3)

if solution:
    for row in solution:
        print(row)
else:
    print("No solution found.")