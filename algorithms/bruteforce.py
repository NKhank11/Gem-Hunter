from createCNF import create_cnf_and_varmap, apply_solution_to_board
from itertools import product
from config import TIME_LIMIT
import time

def solve(board):
    # Create CNF clauses and variable mapping
    clauses, var_map = create_cnf_and_varmap(board)
    
    if not clauses:
        print("Không thể tạo CNF, có thể do bài toán không có lời giải.")
        return board

    # Get the list of variables to assign (which are the variables corresponding to the '_')
    blank_vars = list(var_map.values())
    num_vars = len(blank_vars)
    
    start_time = time.time()

    for assignment in product([0, 1], repeat=num_vars):
        if time.time() - start_time > TIME_LIMIT:
            print(f"Brute-force quá {TIME_LIMIT} giây, dừng lại.")
            return board
        
        # Mapping the assignment to the variables
        assignments = {blank_vars[i]: assignment[i] for i in range(num_vars)}

        satisfies_all = all(
            any((assignments.get(abs(lit), 0) == 1) == (lit > 0) for lit in clause)
            for clause in clauses
        )

        if satisfies_all:
            true_vars = {var for var, val in assignments.items() if val == 1}
            return apply_solution_to_board(board, true_vars, var_map)
    
    print("Không tìm thấy lời giải bằng brute-force.")
    return board