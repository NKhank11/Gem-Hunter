from itertools import combinations, product

def get_neighbors(i, j, board):
    n, m = len(board), len(board[0])
    neighbors = []
    for dx, dy in product([-1, 0, 1], repeat=2):
        if dx == 0 and dy == 0:
            continue
        ni, nj = i + dx, j + dy
        if 0 <= ni < n and 0 <= nj < m:
            neighbors.append((ni, nj))
    return neighbors

def create_cnf_and_varmap(board):
    n, m = len(board), len(board[0])
    clauses = []
    var_map = {}
    reverse_map = {} # Map variable to coordinates
    var_id = 1
    
    # Only consider cells with '_'
    for i in range(n):
        for j in range(m):
            if board[i][j] == '_':
                var_map[(i, j)] = var_id
                reverse_map[var_id] = (i, j)
                var_id += 1

    # Process cells with numbers
    for i in range(n):
        for j in range(m):
            # Handle both int and string number cases
            if isinstance(board[i][j], int) or (isinstance(board[i][j], str) and board[i][j].isdigit()):
                k = int(board[i][j]) if isinstance(board[i][j], int) else int(board[i][j])
                neighbors = get_neighbors(i, j, board)

                # Classify neighboring cells
                hidden_vars = []
                known_traps = 0
                for ni, nj in neighbors:
                    if board[ni][nj] == '_':
                        hidden_vars.append(var_map[(ni, nj)])
                    elif board[ni][nj] == 'T':
                        known_traps += 1

                # Adjust the number of traps to place
                k -= known_traps
                
                # Check validity    
                if k < 0 or k > len(hidden_vars):
                    return [], {}  # No solution

                # Only create constraints if there are hidden cells
                if hidden_vars:
                    # Clauses for at most k traps
                    if k < len(hidden_vars):
                        for combo in combinations(hidden_vars, k + 1):
                            clauses.append([-v for v in combo])

                    # Clauses for at least k traps
                    if k > 0:
                        for combo in combinations(hidden_vars, len(hidden_vars) - k + 1):
                            clauses.append(list(combo))
    
    # Remove duplicate clauses
    unique_clauses = []
    seen = set()
    for clause in clauses:
        tuple_clause = tuple(sorted(clause))
        if tuple_clause not in seen:
            unique_clauses.append(clause)
            seen.add(tuple_clause)
    
    return unique_clauses, var_map

def apply_solution_to_board(board, solution, var_map):
    result = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            if board[i][j] == '_':
                var_id = var_map.get((i, j))
                # Check if the variable is in the solution
                if var_id in solution:
                    row.append('T')  # Trap
                else:
                    row.append('G')  # Gem
            else:
                row.append(board[i][j])
        result.append(row)
    return result