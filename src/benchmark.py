import time
import cProfile
import pstats
import io
from memory_profiler import memory_usage
from reference_avl_tree import AVLTreeReference
from array_avl_tree import AVLTreeArray
from visualize_tree import visualize_tree  # Import the visualization function

def load_dataset(file_path):
    """
    Load the dataset from a file.
    Each line in the file represents an integer to insert into the AVL tree.
    """
    with open(file_path, "r") as f:
        return [int(line.strip()) for line in f.readlines()]

def profile_operation(tree, dataset, operation, is_reference=False):
    """
    Profile a given operation (insert, search, delete) for the given tree.
    """
    times = []
    mem_usage = []

    for key in dataset:
        start_time = time.perf_counter()
        mem_start = memory_usage(-1, interval=0.01, timeout=1)


        if operation == "insert":
            if is_reference:
                tree.root = tree.insert(tree.root, key)
            else:
                tree.insert(key)
        elif operation == "search":
            if is_reference:
                tree.search(tree.root, key)
            else:
                tree.search(key)
        elif operation == "delete":
            if is_reference:
                tree.root = tree.delete(tree.root, key)
            else:
                tree.delete(key)

        mem_end = memory_usage(-1, interval=0.1, timeout=1)
        operation_time = time.perf_counter() - start_time

        times.append(operation_time)
        mem_usage.append(mem_end[0] - mem_start[0])

    return times, mem_usage

def benchmark_operations_with_profiling(tree, dataset, is_reference=False):
    """
    Benchmark operations (insert, search, delete) with profiling for the given tree.
    """
    results = {}
    for operation in ["insert", "search", "delete"]:
        print(f"Profiling {operation} operation for {'Reference' if is_reference else 'Array'}-based AVL Tree...")
        times, mem_usage = profile_operation(tree, dataset, operation, is_reference)
        results[operation] = {
            "times": times,
            "memory": mem_usage
        }

        # Visualize the tree after each operation (optional, can be commented out if not needed)
        visualize_tree(tree, tree_type="Reference" if is_reference else "Array", operation=operation)


    return results

def run_benchmarks_with_profiling():
    """
    Run the benchmarks with detailed profiling for different dataset sizes and tree types.
    """
    datasets = ["../datasets/dataset_small.txt", "../datasets/dataset_medium.txt", "../datasets/dataset_large.txt"]
    results = {"ReferenceAVL": [], "ArrayAVL": []}

    for dataset_path in datasets:
        dataset = load_dataset(dataset_path)

        # Reference-based AVL Tree profiling
        ref_avl = AVLTreeReference()
        print(f"Benchmarking Reference-based AVL Tree with dataset: {dataset_path}")
        ref_results = benchmark_operations_with_profiling(ref_avl, dataset, is_reference=True)
        results["ReferenceAVL"].append(ref_results)

        # Array-based AVL Tree profiling
        array_avl = AVLTreeArray()
        print(f"Benchmarking Array-based AVL Tree with dataset: {dataset_path}")
        array_results = benchmark_operations_with_profiling(array_avl, dataset)
        results["ArrayAVL"].append(array_results)

    # Save results to a file
    with open("../result/benchmark_results.txt", "w") as f:
     for tree_type, tree_results in results.items():
        for idx, dataset_results in enumerate(tree_results):
            dataset_name = datasets[idx].split("/")[-1]  # Get dataset name
            f.write(f"{tree_type} - Dataset: {dataset_name}\n")
            for operation, data in dataset_results.items():
                f.write(f"{operation.capitalize()} Operation:\n")
                f.write(f"  Times: {data['times']}\n")
                f.write(f"  Memory Usage: {data['memory']}\n\n")


    return results

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    # Run the benchmark and profiling
    results = run_benchmarks_with_profiling()

    profiler.disable()

    # Save profiling stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.TIME)
    ps.print_stats()

    with open("../result/profiling_stats.txt", "w") as f:
        f.write(s.getvalue())

    print("Benchmarking and profiling complete. Results saved to benchmark_results.txt and profiling_stats.txt.")
