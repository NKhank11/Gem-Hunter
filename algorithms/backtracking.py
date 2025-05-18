from createCNF import create_cnf_and_varmap, apply_solution_to_board
import time
from config import TIME_LIMIT

def solve(board):
    # Create CNF clauses and variable mapping
    clauses, var_map = create_cnf_and_varmap(board)

    if not clauses:
        print("Không thể tạo CNF, có thể do bài toán không có lời giải.")
        return board

    # Get the list of variables to assign (which are the variables corresponding to the '_')
    blank_vars = list(var_map.values())

    start_time = time.time()

    def is_satisfied(clause, assignment):
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                continue
            if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                return True
        if all(abs(lit) in assignment for lit in clause):
            return False
        return True

    def backtrack(index, assignment):
        # Giới hạn thời gian
        if time.time() - start_time > TIME_LIMIT:
            print(f"Thời gian chạy Backtracking vượt quá {TIME_LIMIT} giây!")
            return "TIMEOUT"

        # Nếu đã gán hết biến
        if index == len(blank_vars):
            # Kiểm tra tất cả mệnh đề
            for clause in clauses:
                if not is_satisfied(clause, assignment):
                    return None
            return assignment

        var = blank_vars[index]

        # Gán True
        assignment[var] = True
        if all(is_satisfied(clause, assignment) for clause in clauses):
            result = backtrack(index + 1, assignment)
            if result == "TIMEOUT":
                return "TIMEOUT"
            if result:
                return result

        # Gán False
        assignment[var] = False
        if all(is_satisfied(clause, assignment) for clause in clauses):
            result = backtrack(index + 1, assignment)
            if result == "TIMEOUT":
                return "TIMEOUT"
            if result:
                return result

        # Quay lui
        del assignment[var]
        return None

    # Bắt đầu đệ quy với biến đầu tiên
    solution = backtrack(0, {})

    if solution == "TIMEOUT":
        return board
    elif solution:
        true_vars = {var for var, val in solution.items() if val}
        return apply_solution_to_board(board, true_vars, var_map)
    else:
        print("Không tìm thấy lời giải bằng backtracking!")
        return board
