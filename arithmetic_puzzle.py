from typing import List, Set, Dict, Tuple, Optional
from collections import defaultdict
import operator
import time
from itertools import product

class ArithmeticPuzzleSolver:
    def __init__(self, n: int, groups: List[Tuple[Set[Tuple[int, int]], str, int]]):
        self.n = n
        self.groups = groups
        self.variables = [(i, j) for i in range(n) for j in range(n)]
        self.domains = {var: set(range(1, n + 1)) for var in self.variables}
        self.constraints = self._create_constraints()

    def _create_constraints(self) -> Dict:
        constraints = defaultdict(list)
        # Row and column constraints
        for i in range(self.n):
            for j in range(self.n):
                # Row constraints
                for k in range(self.n):
                    if k != j:
                        constraints[(i,j)].append(((i,k), lambda x, y: x != y))
                # Column constraints
                for k in range(self.n):
                    if k != i:
                        constraints[(i,j)].append(((k,j), lambda x, y: x != y))

        # Group arithmetic constraints
        for cells, op, target in self.groups:
            for cell in cells:
                constraints[cell].extend([
                    (other_cell, lambda x, y, op=op, cells=cells, target=target:
                     self._check_group_constraint(x, y, op, cells, target))
                    for other_cell in cells if other_cell != cell
                ])
        return constraints

    def _check_group_constraint(self, x: int, y: int, op: str,
                                    cells: Set[Tuple[int, int]], target: int) -> bool:
            ops = {
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.truediv,
                'div': operator.truediv,
                'mult': operator.mul,
                'sub': operator.sub,
                'add': operator.add,
                '': lambda x, y: x  # For single cell groups
            }

            if op == '':
                # Single cell group: must match the target exactly
                return x == target

            if len(cells) == 2:
                # Two-cell group
                if op in ['sub', '-']:
                    return abs(x - y) == target
                elif op in ['div', '/']:
                    # Avoid division-by-zero
                    if x == 0 or y == 0:
                        return False
                    return max(x, y) / min(x, y) == target
                else:
                    # +, add, *, mult
                    op_func = ops[op]
                    return op_func(x, y) == target

            # -----------------------------
            # STRONGER CHECK FOR 3+ CELLS
            # -----------------------------
            # Instead of just "x*y <= target", do a full combination check.
            # We see if ANY combination of values in these cells' domains
            # can satisfy the cage constraint while also having
            # the pair of cells forced to x and y.
            cell_list = list(cells)

            # We'll figure out which indices correspond to the two cells
            # in the current arc (we have them as arcs xi->xj in AC3).
            # Because each call is pairwise, we do not directly know
            # which (xi, xj) we are. But we know that "x" must belong
            # to the 'cell' we're currently revising, and "y" must belong
            # to 'other_cell'. We'll trust that code is consistent with AC3.
            #
            # We'll just go ahead and try to find ANY assignment that
            # respects "cell_list[i1] has value x" and "cell_list[i2] has value y"
            # that yields the correct group operation result.
            #
            # If none works, we return False => prune.

            # For the sake of checking, let's gather each cell's domain:
            domain_list = [self.domains[c] for c in cell_list]

            # We'll try every possible combination from domain_list
            # that places x in one cell and y in another cell:
            def cage_ok(values: List[int]) -> bool:
                """ Check if the entire 'values' assignment for this cage satisfies op==target. """
                if op in ['mult','*']:
                    prod = 1
                    for v in values:
                        prod *= v
                    return prod == target
                elif op in ['add','+']:
                    return sum(values) == target
                elif op in ['sub','-']:
                    # For 3+ cells, KenKen typically doesn't use sub on 3+ cells,
                    # but if it did, you'd define the extension. For now, skip or handle similarly
                    # e.g. pick all permutations, or define a rule. We'll skip for clarity.
                    return True
                elif op in ['div','/']:
                    # Similarly, doesn't normally happen with 3+ cells; skipping here.
                    return True
                return True

            # We must place x,y into the correct positions. There are exactly 2 cells in the
            # cage for our current arc. We'll locate them first:
            # (This is a hacky approach that works in typical AC3 code. Adjust if needed.)
            # We'll search for any valid assignment that matches x,y appropriately.
            valid_combo_found = False

            # For each combination from the Cartesian product of domain_list
            # consider them as an assignment to cell_list in order
            # but we also must ensure that the two specific cells
            # in the "arc" get x, y respectively.
            for combo in product(*domain_list):
                # 'combo' is a tuple of length len(cells),
                # combo[i] is the value assigned to cell_list[i].
                # We check if x and y are assigned to the correct pair.

                # We'll grab indexes of the pair in cell_list
                # that correspond to the "current arc" (some AC3 calls).
                # AC3 code calls _check_group_constraint with x,y for a certain pair,
                # but we only know that "cell" is the first and "other_cell" the second.
                # Because this code is reused for each arc, let's do a quick check:
                #   - 'cell' is the one that triggered this run.
                #   - 'other_cell' is the neighbor.
                # We'll find them:
                # But the function signature doesn't have 'cell' or 'other_cell' explicitly
                # other than in that constraints creation. Let's do a small trick:
                # We'll just see if x can appear in exactly one position and y in exactly one position
                # among the combo (which must be distinct positions).
                # For KenKen, we expect all digits in one cage to be distinct if they share row/col, but
                # we won't fully enforce that here—just the cage arithmetic.

                # A simpler approach is: as soon as AC3 calls us with x,y, it wants to see
                # if there's ANY scenario in which x,y is feasible. We'll check if x,y can appear
                # in two distinct cells of 'cells'. (In real GAC you'd track exact arcs, but let's keep it minimal.)

                # Count how many times x appears in combo, how many times y appears in combo:
                # If x,y appear at least once (and in different positions if x!=y), we can check the final arithmetic.

                # However, to be sure that the 'arc' is truly consistent, we do:
                #   - Exactly one position in combo = x if x != y
                #   - Another position in combo = y
                #   - If x == y, then we just need at least two positions that are x.

                # This is not a perfect approach for big puzzles with repeated digits in the same cage,
                # but standard 4x4 KenKen doesn't allow repeated digits in a single row/col,
                # so let's keep it simple.

                if x != y:
                    # We only require that x and y each appear at least once
                    # so that (xi->x, xj->y) is reflected in 'combo'.
                    if combo.count(x) >= 1 and combo.count(y) >= 1:
                        if cage_ok(combo):
                            valid_combo_found = True
                            break
                else:
                    # x == y case; we want at least two cells in the cage that have that same value
                    # e.g., if x=2, y=2. We need 2 positions in combo that have '2'
                    if combo.count(x) >= 2 and cage_ok(combo):
                        valid_combo_found = True
                        break

            if not valid_combo_found:
                # No valid set of values in the entire cage that includes x, y and yields target
                return False

            return True
        # (end of _check_group_constraint, rest of the class is unchanged)
        
    def ac3(self) -> bool:
        for cells, op, target in self.groups:
            if len(cells) == 1:  # Single-cell group
                cell = next(iter(cells))  # Get the single element from the set
                self.domains[cell] = {target}  # Restrict its domain to the target number
        # AC-3 algorithm for domain reduction before backtracking
        queue = [(xi, xj) for xi in self.variables for xj, _ in self.constraints[xi]]
        while queue:
            xi, xj = queue.pop(0)
            if self._revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk, _ in self.constraints[xi]:  # Fixed: Added proper tuple unpacking
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
        revised = False
        # For each constraint on xi that involves xj
        for constraint in self.constraints[xi]:
            if constraint[0] == xj:
                # For each value in xi's domain
                for x in self.domains[xi].copy():
                    # If there's no value in xj's domain that satisfies the constraint, remove x
                    if not any(constraint[1](x, y) for y in self.domains[xj]):
                        self.domains[xi].remove(x)
                        revised = True
        return revised
    


    def mrv(self, assignment: Dict[Tuple[int, int], int]) -> Optional[Tuple[int, int]]:
        # Minimum Remaining Values heuristic
        unassigned = [(var, len(self.domains[var]))
                      for var in self.variables if var not in assignment]
        return min(unassigned, key=lambda x: x[1])[0] if unassigned else None

    def forward_check(self, var: Tuple[int, int], value: int, assignment: Dict) -> bool:
        """
        Forward-check: remove values from neighbors' domains that violate constraints
        given 'var' is assigned 'value'.
        """
        for neighbor, constraint in self.constraints[var]:
            if neighbor not in assignment:
                for val in self.domains[neighbor].copy():
                    if not constraint(value, val):
                        self.domains[neighbor].remove(val)
                if not self.domains[neighbor]:
                    return False
        return True

    def _is_consistent(self, var: Tuple[int, int], value: int, assignment: Dict) -> bool:
        """
        Basic consistency check for newly assigned var=value,
        ensuring row/column uniqueness and fully assigned group constraints.
        """
        row, col = var
        # Row/column uniqueness
        for i in range(self.n):
            # Same row
            if (row, i) in assignment and i != col and assignment[(row, i)] == value:
                return False
            # Same column
            if (i, col) in assignment and i != row and assignment[(i, col)] == value:
                return False

        # If all cells in a group become assigned, check final group constraints
        for cells, op, target in self.groups:
            if var in cells:
                group_values = {cell: assignment[cell] for cell in cells if cell in assignment}
                group_values[var] = value

                if len(group_values) == len(cells):  # all assigned
                    values = list(group_values.values())
                    if op in ['sub', '-']:
                        if len(values) == 2 and abs(values[0] - values[1]) != target:
                            return False
                    elif op in ['div', '/']:
                        if len(values) == 2:
                            if 0 in values:
                                return False
                            ma = max(values)
                            mi = min(values)
                            if ma / mi != target:
                                return False
                    elif op in ['mult', '*']:
                        prod = 1
                        for v in values:
                            if v == 0:
                                return False
                            prod *= v
                        if prod != target:
                            return False
                    elif op in ['add', '+']:
                        if sum(values) != target:
                            return False
                    elif op == '':
                        if values[0] != target:
                            return False

        return True

    def _backtrack(self, assignment: Dict[Tuple[int, int], int]) -> Optional[Dict[Tuple[int, int], int]]:
        """
        Standard Backtracking (used by solve(..., algorithm="backtracking") or after AC3)
        """
        if len(assignment) == len(self.variables):
            return assignment

        var = self.mrv(assignment)
        if var is None:
            return None

        for value in self.domains[var].copy():
            if self._is_consistent(var, value, assignment):
                assignment[var] = value
                # Save current domains
                old_domains = {v: self.domains[v].copy() for v in self.variables}

                if self.forward_check(var, value, assignment):
                    result = self._backtrack(assignment)
                    if result is not None:
                        return result

                # Revert domain changes
                self.domains = old_domains
                del assignment[var]

        return None

    def backtrack(self) -> Optional[Dict[Tuple[int, int], int]]:
        """
        Public method to run standard backtracking.
        """
        return self._backtrack({})

    def _forward_checking_search(self, assignment: Dict[Tuple[int,int], int]) -> Optional[Dict[Tuple[int,int], int]]:
        """
        Recursively assign variables with forward checking at each step.
        """
        if len(assignment) == len(self.variables):
            return assignment

        var = self.mrv(assignment)
        if var is None:
            return None

        for value in self.domains[var].copy():
            if self._is_consistent(var, value, assignment):
                assignment[var] = value

                # Save original domains so we can revert after forward checking
                saved_domains = {v: self.domains[v].copy() for v in self.variables}

                # If forward checking succeeds, recurse
                if self.forward_check(var, value, assignment):
                    result = self._forward_checking_search(assignment)
                    if result is not None:
                        return result

                # Revert domains and remove assignment
                self.domains = saved_domains
                del assignment[var]

        return None

    def forward_checking(self) -> Optional[Dict[Tuple[int,int], int]]:
        """
        Public method to run forward-checking-based solver.
        """
        return self._forward_checking_search({})
    
    def _backtrack_no_forward_check(self, assignment: Dict[Tuple[int, int], int]) -> Optional[Dict[Tuple[int, int], int]]:
        if len(assignment) == len(self.variables):
            return assignment  # Found a complete assignment

        var = self.mrv(assignment)
        if var is None:
            return None

        # Iterate possible values for var
        for value in self.domains[var].copy():
            if self._is_consistent(var, value, assignment):
                assignment[var] = value

                # Recurse without forward checking
                result = self._backtrack_no_forward_check(assignment)
                if result is not None:
                    return result

                # Revert if failed
                del assignment[var]

        return None
    def backtrack_no_forward_check(self) -> Optional[Dict[Tuple[int, int], int]]:
        """
        Public method that uses pure backtracking (i.e., NO forward checking).
        """
        # You might (optionally) restore original domains first if needed
        # e.g. self.domains = {var: set(range(1, self.n + 1)) for var in self.variables}
        return self._backtrack_no_forward_check({})

    def solve(self, algorithm: str = "ac3+backtracking") -> Optional[Dict[Tuple[int, int], int]]:
        """
        Solve the puzzle using different algorithms:
        - "ac3": run AC3 only
        - "ac3+backtracking": run AC3, then backtracking
        - "backtracking": standard backtracking only
        - "backtracking_no_forward_check": backtracking without forward checking
        """

        print(f"Solving with {algorithm}...")
        if algorithm == "ac3":
            success = self.ac3()
            print("\nDomains after AC3:")
            for i in range(self.n):
                for j in range(self.n):
                    print(f"Cell ({i},{j}): {sorted(self.domains[(i,j)])}")
            return success
        
        if algorithm == "ac3+backtracking":
            if self.ac3():
                print("\nDomains after AC3:")
                for i in range(self.n):
                    for j in range(self.n):
                        print(f"Cell ({i},{j}): {sorted(self.domains[(i,j)])}")
                return self.backtrack()
            return None
        elif algorithm == "backtracking":
            return self.backtrack()
        elif algorithm == "backtracking_no_fc":
            return self.backtrack_no_forward_check()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")