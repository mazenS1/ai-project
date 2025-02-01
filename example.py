from arithmetic_puzzle import ArithmeticPuzzleSolver
import time
import numpy as np

def main():
    n1 = 6
    groups1 = [
        ({(0,0), (1,0)}, 'sub', 4),
        ({(0,1), (1,1)}, 'sub', 1),
        ({(0,2), (0,3)}, 'sub', 3),
        ({(0,4), (0,5)}, 'div', 3),
        ({(1,2), (1,3)}, 'sub', 1),
        ({(1,4), (1,5), (2,4)}, 'mult', 150),
        ({(2,0), (2,1), (3,0)}, 'add', 7),
        ({(2,2), (2,3)}, 'sub', 2),
        ({(2,5), (3,5)}, 'add', 5),
        ({(3,1), (3,2)}, 'sub', 1),
        ({(3,3), (3,4)}, 'div', 3),
        ({(4,0)}, '', 3),
        ({(4,1), (4,2), (5,2)}, 'mult', 60),
        ({(4,3), (5,3)}, 'sub', 4),
        ({(4,4), (5,4)}, 'sub', 1),
        ({(4,5), (5,5)}, 'sub', 3),
        ({(5,0), (5,1)}, 'div', 3),
    ]
    n2 = 4
    groups2 = [
        ({(0,0), (0,1), (1,0)}, 'mult', 24),
        ({(0,2), (0,3)}, 'div', 2),
        ({(1,1), (1,2)}, 'sub', 3),
        ({(1,3), (2,3)}, 'sub', 1),
        ({(2,0), (2,1)}, 'add', 5),
        ({(3,0), (3,1)}, 'sub', 3),
        ({(2,2), (3,2), (3,3)}, 'add', 6),
    ]
    n3 = 9
    groups3=[
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
        ({(6,0), (7,0)}, 'div', 4),
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
    
    
    algorithm = 'ac3+backtracking'
    solver = ArithmeticPuzzleSolver(n3, groups3)
    start_time = time.time()
    solution = solver.solve(algorithm)
    print(f"Time taken: {time.time() - start_time:.8f} seconds")

    if algorithm == 'ac3':
        pass
    elif solution:
        print("\nSolution:")
        print("-" * (n3 * 4 - 1))
        for i in range(n3):
            row = [str(solution.get((i, j), '.')) for j in range(n3)]
            print("|" + "|".join(f" {x} " for x in row) + "|")
            print("-" * (n3 * 4 - 1))
    else:
        print("No solution exists using algorithm X with constraints propagation.")



n3 = 9
groups3=[
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
    ({(6,0), (7,0)}, 'div', 4),
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
n1 = 6
groups1 = [
    ({(0,0), (1,0)}, 'sub', 4),
    ({(0,1), (1,1)}, 'sub', 1),
    ({(0,2), (0,3)}, 'sub', 3),
    ({(0,4), (0,5)}, 'div', 3),
    ({(1,2), (1,3)}, 'sub', 1),
    ({(1,4), (1,5), (2,4)}, 'mult', 150),
    ({(2,0), (2,1), (3,0)}, 'add', 7),
    ({(2,2), (2,3)}, 'sub', 2),
    ({(2,5), (3,5)}, 'add', 5),
    ({(3,1), (3,2)}, 'sub', 1),
    ({(3,3), (3,4)}, 'div', 3),
    ({(4,0)}, '', 3),
    ({(4,1), (4,2), (5,2)}, 'mult', 60),
    ({(4,3), (5,3)}, 'sub', 4),
    ({(4,4), (5,4)}, 'sub', 1),
    ({(4,5), (5,5)}, 'sub', 3),
    ({(5,0), (5,1)}, 'div', 3),
]
n2 = 4
groups2 = [
    ({(0,0), (0,1), (1,0)}, 'mult', 24),
    ({(0,2), (0,3)}, 'div', 2),
    ({(1,1), (1,2)}, 'sub', 3),
    ({(1,3), (2,3)}, 'sub', 1),
    ({(2,0), (2,1)}, 'add', 5),
    ({(3,0), (3,1)}, 'sub', 3),
    ({(2,2), (3,2), (3,3)}, 'add', 6),
]


# TODO: write a function to run each problem 10 times for each algorithm and record the best/worst/average time, then plot the results
def run_experiment():
    algorithms = ['ac3+backtracking', 'backtracking_no_fc']
    problems = [(n1, groups1), (n2, groups2), (n3, groups3)]
    results = {}
    for n, groups in problems:
        for algorithm in algorithms:
            solver = ArithmeticPuzzleSolver(n, groups)
            times = []
            for i in range(3):
                start_time = time.time()
                solution = solver.solve(algorithm)
                times.append(time.time() - start_time)
            best_time = min(times)
            worst_time = max(times)
            avg_time = sum(times) / len(times)
            results[(n, algorithm)] = (best_time, worst_time, avg_time)
    return results



def plot_results(results):
    import matplotlib.pyplot as plt

    # Organize data by size (n)
    sizes = sorted(list(set(n for n, _ in results.keys())))
    algorithms = sorted(list(set(alg for _, alg in results.keys())))
    
    # Set up plot
    width = 0.25
    x = np.arange(len(sizes))
    _, ax = plt.subplots(figsize=(12, 6))
    
    # Plot bars for each algorithm
    for i, alg in enumerate(algorithms):
        avg_times = [results[(n, alg)][2] for n in sizes]  # Using average times
        ax.bar(x + i*width, avg_times, width, label=alg)
        
        # Add error bars
        min_times = [results[(n, alg)][0] for n in sizes]
        max_times = [results[(n, alg)][1] for n in sizes]
        error_low = [avg - min_t for avg, min_t in zip(avg_times, min_times)]
        error_high = [max_t - avg for max_t, avg in zip(max_times, avg_times)]
        ax.errorbar(x + i*width, avg_times, yerr=[error_low, error_high], 
                   fmt='none', color='black', capsize=5)
    
    # Customize plot
    ax.set_yscale('log')  # Use logarithmic scale for better visibility
    ax.set_ylabel('Time (seconds)')
    ax.set_xlabel('Puzzle Size')
    ax.set_title('Algorithm Performance by Puzzle Size')
    ax.set_xticks(x + width)
    ax.set_xticklabels(sizes)
    ax.legend()
    ax.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.show()

def main2():
    results = run_experiment()
    for key in results:
        print(key, results[key])
    plot_results(results)

if __name__ == "__main__":
    main2()
