import os
import time
from algorithms.pysat import solve as solve_with_pysat
from algorithms.bruteforce import solve as solve_with_bruteforce
from algorithms.backtracking import solve as solve_with_backtracking
from config import TIME_LIMIT

def read_board(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    board = []
    for line in lines:
        if line.strip():  # Skip empty lines
            row = [cell.strip() for cell in line.strip().split(',')]
            board.append(row)
    
    return board

def write_combined_results(file_path, board, results):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("=== KẾT QUẢ CÁC THUẬT TOÁN ===\n")
        # PySAT
        f.write("\n--- PySAT ---\n")
        if results['pysat']['timeout']:
            f.write(f"Thời gian chạy: Quá {TIME_LIMIT} giây - thuật toán đã dừng\n")
        else:
            for row in results['pysat']['board']:
                f.write(', '.join(row) + '\n')
            f.write(f"Thời gian chạy: {results['pysat']['duration']:.4f} giây\n")
        
        # Backtracking
        f.write("\n--- Backtracking ---\n")
        if results['backtracking']['timeout']:
            f.write(f"Thời gian chạy: Quá {TIME_LIMIT} giây - thuật toán đã dừng\n")
        else:
            for row in results['backtracking']['board']:
                f.write(', '.join(row) + '\n')
            f.write(f"Thời gian chạy: {results['backtracking']['duration']:.4f} giây\n")
                    
        # Brute-force
        f.write("\n--- Brute-force ---\n")
        if results['bruteforce']['timeout']:
            f.write(f"Thời gian chạy: Quá {TIME_LIMIT} giây - thuật toán đã dừng\n")
        else:
            for row in results['bruteforce']['board']:
                f.write(', '.join(row) + '\n')
            f.write(f"Thời gian chạy: {results['bruteforce']['duration']:.4f} giây\n")
        


def print_board(board):
    for row in board:
        print(', '.join(row))

def run_solver_with_timeout(algorithm_func, board, time_limit=TIME_LIMIT):
    start_time = time.time()
    result_board = board 
    timed_out = False
    
    try:
        # Implement algorithm
        result_board = algorithm_func(board)
        end_time = time.time()
        duration = end_time - start_time
        
        # Check duration
        if duration > time_limit:
            timed_out = True
            print(f"Thời gian chạy quá {time_limit} giây! Thuật toán đã dừng.")
        else:
            print(f"Thời gian chạy: {duration:.4f} giây")
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"Lỗi: {e}")
        if duration > time_limit:
            timed_out = True
            print(f"Thời gian chạy quá {time_limit} giây!")
    
    return result_board, (end_time - start_time), timed_out

def main():
    input_dir = "testcases/input/"
    output_dir = "testcases/output/"
    
    # Ensure directories exist
    os.makedirs(output_dir, exist_ok=True)

    print("Chọn file input:")
    print("1. input_1.txt")
    print("2. input_2.txt")
    print("3. input_3.txt")
    
    while True:
        file_choice = input("Nhập lựa chọn (1/2/3): ")
        if file_choice in ['1', '2', '3']:
            break
        print("Lựa chọn không hợp lệ! Vui lòng nhập lại.")

    input_path = os.path.join(input_dir, f"input_{file_choice}.txt")
    
    if not os.path.exists(input_path):
        print(f"File {input_path} không tồn tại!")
        return

    # Read the board from the input file
    board = read_board(input_path)
    print(f"\n--- Bài toán ---")
    print_board(board)

    # Initialize results dictionary
    results = {
        'pysat': {'board': None, 'duration': 0, 'timeout': False},
        'bruteforce': {'board': None, 'duration': 0, 'timeout': False},
        'backtracking': {'board': None, 'duration': 0, 'timeout': False}
    }
    
    # PySAT
    print("\n--- PySAT ---")
    result_pysat, duration_pysat, timeout_pysat = run_solver_with_timeout(solve_with_pysat, board)
    results['pysat']['board'] = result_pysat
    results['pysat']['duration'] = duration_pysat
    results['pysat']['timeout'] = timeout_pysat
    
    if not timeout_pysat:
        print_board(result_pysat)
   
    # Backtracking
    print("\n--- Backtracking ---")
    result_bt, duration_bt, timeout_bt = run_solver_with_timeout(solve_with_backtracking, board)
    results['backtracking']['board'] = result_bt
    results['backtracking']['duration'] = duration_bt
    results['backtracking']['timeout'] = timeout_bt
    
    if not timeout_bt:
        print_board(result_bt)

    # Brute-force
    print("\n--- Brute-force ---")
    result_bf, duration_bf, timeout_bf = run_solver_with_timeout(solve_with_bruteforce, board)
    results['bruteforce']['board'] = result_bf
    results['bruteforce']['duration'] = duration_bf
    results['bruteforce']['timeout'] = timeout_bf
    
    if not timeout_bf:
        print_board(result_bf)
    
    # Save all results to a file
    output_path = os.path.join(output_dir, f"output_{file_choice}.txt")
    write_combined_results(output_path, board, results)
    print(f"\nĐã lưu tất cả kết quả vào file {output_path}")
    
    # Print summary
    print("\n=== Kết quả thời gian chạy ===")
    print(f"PySAT: {'Quá ' + str(TIME_LIMIT) + ' giây' if timeout_pysat else f'{duration_pysat:.4f} giây'}")
    print(f"Backtracking: {'Quá ' + str(TIME_LIMIT) + ' giây' if timeout_bt else f'{duration_bt:.4f} giây'}")
    print(f"Brute-force: {'Quá ' + str(TIME_LIMIT) + ' giây' if timeout_bf else f'{duration_bf:.4f} giây'}")


if __name__ == "__main__":
    main()