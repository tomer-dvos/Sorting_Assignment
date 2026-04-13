import time
import random
import statistics
import matplotlib.pyplot as plt
import argparse

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr


def generate_array(size, array_type="random", noise_level=0):
    if array_type == "random":
        return [random.randint(1, 10000) for _ in range(size)]

    elif array_type == "nearly_sorted":
        arr = list(range(size))
        num_swaps = int(size * (noise_level / 100.0))
        for _ in range(num_swaps):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


def run_experiment(algorithms, sizes, repeats, array_type="random", noise_level=0):
    results = {algo.__name__: {"avg": [], "std": []} for algo in algorithms}

    for size in sizes:
        print(f"Running size {size}...")
        test_arrays = [generate_array(size, array_type, noise_level) for _ in range(repeats)]

        for algo in algorithms:
            times = []
            for i in range(repeats):
                arr_copy = test_arrays[i].copy()

                start_time = time.time()
                algo(arr_copy)
                end_time = time.time()

                times.append(end_time - start_time)

            avg_time = statistics.mean(times)
            std_dev = statistics.stdev(times) if repeats > 1 else 0.0

            results[algo.__name__]["avg"].append(avg_time)
            results[algo.__name__]["std"].append(std_dev)

    return results


def plot_results(results, sizes, title, filename):
    plt.figure(figsize=(10, 6))

    for algo_name, data in results.items():
        avgs = data["avg"]
        stds = data["std"]

        plt.plot(sizes, avgs, marker='o', label=algo_name)

        upper_bound = [a + s for a, s in zip(avgs, stds)]
        lower_bound = [max(0, a - s) for a, s in zip(avgs, stds)]
        plt.fill_between(sizes, lower_bound, upper_bound, alpha=0.2)

    plt.title(title)
    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.savefig(filename)
    print(f"Saved plot to {filename}")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sorting Algorithms Experiment Runner")
    parser.add_argument("-a", type=int, nargs='+', required=True,
                        help="Algorithms: 1=Bubble, 2=Selection, 4=Merge")
    parser.add_argument("-s", type=int, nargs='+', required=True, help="Array sizes (e.g., 100 500 1000)")
    parser.add_argument("-e", type=int, choices=[1, 2], required=True,
                        help="Experiment type: 1 (5% noise) or 2 (20% noise)")
    parser.add_argument("-r", type=int, required=True, help="Number of repetitions")

    args = parser.parse_args()

    algo_dict = {
        1: bubble_sort,
        2: selection_sort,
        4: merge_sort
    }

    unsupported_algorithms = sorted({alg_id for alg_id in args.a if alg_id not in algo_dict})
    if unsupported_algorithms:
        supported_ids = ", ".join(str(alg_id) for alg_id in sorted(algo_dict))
        bad_ids = ", ".join(str(alg_id) for alg_id in unsupported_algorithms)
        print(f"Error: Unsupported algorithm ID(s): {bad_ids}. Supported IDs are: {supported_ids}.")
        exit(1)

    selected_algorithms = [algo_dict[alg_id] for alg_id in args.a]

    if not selected_algorithms:
        print("Error: None of the selected algorithms are implemented.")
        exit(1)

    print("--- Running Command Line Experiment (Random Arrays) ---")
    random_results = run_experiment(selected_algorithms, args.s, args.r, "random")
    plot_results(random_results, args.s, "Runtime Comparison (Random Arrays)", "result1.png")

    noise_level = 5 if args.e == 1 else 20

    print(f"--- Running Command Line Experiment (Nearly Sorted, noise={noise_level}%) ---")

    cli_results = run_experiment(selected_algorithms, args.s, args.r, "nearly_sorted", noise_level)

    plot_results(cli_results, args.s, f"Runtime Comparison (Nearly Sorted, noise={noise_level}%)", "result2.png")
