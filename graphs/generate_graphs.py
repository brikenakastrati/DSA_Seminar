import matplotlib.pyplot as plt
import os

def load_results(file_path):
    """
    Load benchmark results from a custom text file format.
    """
    results = {}
    with open(file_path, "r") as f:
        lines = f.readlines()

    current_tree_type = None
    current_dataset = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if " - Dataset: " in line:
            current_tree_type, current_dataset = line.split(" - Dataset: ")
            current_dataset = current_dataset.strip()
            if current_tree_type not in results:
                results[current_tree_type] = {}
            results[current_tree_type][current_dataset] = {}

        elif line.endswith("Operation:"):
            operation = line.replace("Operation:", "").strip().lower()
            results[current_tree_type][current_dataset][operation] = {"times": [], "memory": []}

        elif line.startswith("Times:"):
            times = list(map(float, line.replace("Times:", "").strip(" []\n").split(", ")))
            results[current_tree_type][current_dataset][operation]["times"] = times

        elif line.startswith("Memory Usage:"):
            memory = list(map(float, line.replace("Memory Usage:", "").strip(" []\n").split(", ")))
            results[current_tree_type][current_dataset][operation]["memory"] = memory

    return results

def plot_time_complexity(results, operations, output_dir="graphs"):
    """
    Plot time complexity for the given operations.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for operation in operations:
        plt.figure(figsize=(10, 6))

        for tree_type, datasets in results.items():
            average_times = []
            dataset_sizes = []

            for dataset_name, dataset in datasets.items():
                times = dataset[operation]["times"]
                average_time = sum(times) / len(times)
                average_times.append(average_time)
                dataset_sizes.append(len(times))

            plt.plot(dataset_sizes, average_times, marker="o", label=tree_type)

        plt.title(f"Time Complexity for {operation.capitalize()} Operation")
        plt.xlabel("Dataset Size")
        plt.ylabel("Average Time (seconds)")
        plt.legend()
        plt.grid()
        plt.savefig(f"{output_dir}/{operation}_time_complexity.png")
        plt.close()

def plot_memory_usage(results, operations, output_dir="graphs"):
    """
    Plot memory usage for the given operations.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for operation in operations:
        plt.figure(figsize=(10, 6))

        for tree_type, datasets in results.items():
            average_memory = []
            dataset_sizes = []

            for dataset_name, dataset in datasets.items():
                memory = dataset[operation]["memory"]
                avg_memory = sum(memory) / len(memory)
                average_memory.append(avg_memory)
                dataset_sizes.append(len(memory))

            plt.plot(dataset_sizes, average_memory, marker="o", label=tree_type)

        plt.title(f"Memory Usage for {operation.capitalize()} Operation")
        plt.xlabel("Dataset Size")
        plt.ylabel("Average Memory Usage (MB)")
        plt.legend()
        plt.grid()
        plt.savefig(f"{output_dir}/{operation}_memory_usage.png")
        plt.close()

def generate_performance_graphs():
    """
    Generate performance graphs for benchmark results.
    """
    results_file = "../result/benchmark_results.txt"  # Path to the custom results file
    output_dir = "graphs"

    # Load the benchmark results
    results = load_results(results_file)

    # Define the operations to analyze
    operations = ["insert", "search", "delete"]

    # Generate time complexity graphs
    print("Generating time complexity graphs...")
    plot_time_complexity(results, operations, output_dir)

    # Generate memory usage graphs
    print("Generating memory usage graphs...")
    plot_memory_usage(results, operations, output_dir)

    print(f"Graphs generated and saved in the {output_dir}/ directory.")

if __name__ == "__main__":
    generate_performance_graphs()
