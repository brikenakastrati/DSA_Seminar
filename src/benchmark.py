import time
import cProfile
import pstats
import io
from memory_profiler import memory_usage
from reference_avl_tree import AVLTreeReference
from array_avl_tree import ArrayAVLTree
import graphviz
import os
import subprocess

def load_dataset(file_path):
    """
    Load the dataset from a file.
    Each line in the file represents an integer to insert into the AVL tree.
    """
    with open(file_path, "r") as f:
        return [int(line.strip()) for line in f.readlines()]

def visualize_tree(tree, tree_type="Reference", operation="Visualization", search_key=None):
    """
    Visualize the AVL tree using Graphviz, with labels for operation and tree type.
    Highlight the path to the search_key if provided.
    """
    dot = graphviz.Digraph(comment='AVL Tree', format='png')

    # Add a title to the graph with operation (insert, delete, search) and tree type
    dot.attr(label=f"AVL Tree - {tree_type} | Operation: {operation}", labelloc="t", fontsize="20")

    if tree_type == "Reference":
        # Handle reference-based AVL tree visualization
        def add_edges(node, parent=None, path=None):
            if node is not None:
                node_id = str(node.key)
                if path and node.key in path:
                    dot.node(node_id, label=str(node.key), color="red", style="filled", fillcolor="lightpink")
                else:
                    dot.node(node_id, label=str(node.key))

                if parent:
                    if path and node.key in path and parent in path:
                        dot.edge(parent, node_id, color="red", penwidth="2.0")
                    else:
                        dot.edge(parent, node_id)

                add_edges(node.left, parent=node_id, path=path)
                add_edges(node.right, parent=node_id, path=path)

        # If it's a search operation and search_key is provided, find the path
        path = []
        if operation == "search" and search_key is not None:
            current = tree.root
            while current:
                path.append(current.key)
                if search_key == current.key:
                    break
                elif search_key < current.key:
                    current = current.left
                else:
                    current = current.right

        add_edges(tree.root, path=path)  # Start visualizing from the root

    elif tree_type == "Array":
        # Handle array-based AVL tree visualization
        def add_edges_from_array(index=0, parent=None, path=None):
            if index >= tree.size or index == -1:
                return
            node_id = str(tree.keys[index])
            if path and tree.keys[index] in path:
                dot.node(node_id, label=str(tree.keys[index]), color="red", style="filled", fillcolor="lightpink")
            else:
                dot.node(node_id, label=str(tree.keys[index]))

            if parent:
                if path and tree.keys[index] in path and parent in path:
                    dot.edge(parent, node_id, color="red", penwidth="2.0")
                else:
                    dot.edge(parent, node_id)

            add_edges_from_array(tree.left[index], node_id, path)
            add_edges_from_array(tree.right[index], node_id, path)

        # If it's a search operation and search_key is provided, find the path
        path = []
        if operation == "search" and search_key is not None:
            current = tree.root
            while current != -1 and current < tree.size:
                path.append(tree.keys[current])
                if search_key == tree.keys[current]:
                    break
                elif search_key < tree.keys[current]:
                    current = tree.left[current]
                else:
                    current = tree.right[current]

        add_edges_from_array(tree.root, path=path)

    # Ensure the output directory exists
    output_dir = r"C:\Users\brike\Desktop\Algoritma\visual"
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename with tree type, operation, and database size
    output_path = get_unique_filename(output_dir, tree_type, operation, ".png")

    # Render the visualization to the specified file path (without the extension, as Graphviz will append '.png')
    render_with_timeout(dot, output_path)

def get_unique_filename(folder, tree_type, operation, extension):
    """
    Generate a unique filename in the specified folder with tree type, operation, and database size.
    """
    counter = 1
    while True:
        filename = f"{tree_type}_{operation}_{counter}{extension}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

def render_with_timeout(dot, output_path, timeout=60):
    try:
        # Render using Graphviz
        dot.render(output_path[:-4], format='png', cleanup=True)
        print(f"Tree visualization saved at {output_path}")
    except subprocess.TimeoutExpired:
        print("Rendering timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Error in rendering: {e}")

def profile_operation(tree, dataset, operation, key=10, is_reference=False):
    """
    Profile a given operation (insert, search, delete) for the given tree.
    The search and delete operations are specifically performed for the provided key (default is 10).
    """
    times = []
    mem_usage = []

    for data_key in dataset:
        start_time = time.perf_counter()
        mem_start = memory_usage(-1, interval=0.01, timeout=1)

        if operation == "insert":
            if is_reference:
                tree.root = tree.insert(tree.root, data_key)
            else:
                tree.insert(data_key)
        elif operation == "search":
            if key and hasattr(tree, 'search'):
                if is_reference:
                    tree.search(tree.root, key)
                else:
                    tree.search(key)
        elif operation == "delete":
            if data_key == key:
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
    tree_type = "Reference" if is_reference else "Array"
    for operation in ["insert", "search", "delete"]:
        print(f"Profiling {operation} operation for {tree_type}-based AVL Tree...")
        times, mem_usage = profile_operation(tree, dataset, operation, key=10, is_reference=is_reference)
        results[operation] = {
            "times": times,
            "memory": mem_usage
        }
        
        # Visualize the tree after each operation
        search_key = 10 if operation == "search" else None
        visualize_tree(tree, tree_type=tree_type, operation=operation, search_key=search_key)

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
        array_avl = ArrayAVLTree()
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
