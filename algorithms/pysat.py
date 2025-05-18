from pysat.solvers import Glucose3
from createCNF import create_cnf_and_varmap, apply_solution_to_board
from config import TIME_LIMIT
import time


def solve(board):
    # Create CNF clauses and variable mapping
    clauses, var_map = create_cnf_and_varmap(board)
    
    if not clauses:
        print("Không thể tạo CNF, có thể do bài toán không có lời giải.")
        return board
    
    # Initialize the SAT solver
    solver = Glucose3()
    
    # Add all clauses to the solver
    for clause in clauses:
        solver.add_clause(clause)

    # Check duration
    start_time = time.time()

    # Solve
    if not solver.solve():
        print("Bài toán không có lời giải!")
        return board

    # Check if duration exceeds limit
    current_time = time.time()
    if current_time - start_time > TIME_LIMIT:
        print(f"Thời gian chạy PySAT vượt quá {TIME_LIMIT} giây!")
        return board
    
    # Get the solution model (variable assignments)
    model = solver.get_model()
    
    # Convert model to a set of positive (true) variables
    true_vars = set(var for var in model if var > 0)

    # Apply the solution to the board
    result_board = apply_solution_to_board(board, true_vars, var_map)
    
    return result_board