# import graphviz
# import os
# import subprocess

# def visualize_tree(tree, tree_type="Reference", operation="Visualization"):
#     """
#     Visualize the AVL tree using Graphviz, with labels for operation and tree type.
#     """
#     dot = graphviz.Digraph(comment='AVL Tree', format='png')

#     # Add a title to the graph with operation (insert, delete, search) and tree type
#     dot.attr(label=f"AVL Tree - {tree_type} | Operation: {operation}", labelloc="t", fontsize="20")

#     if tree_type == "Reference":
#         # Handle reference-based AVL tree visualization
#         def add_edges(node, parent=None):
#             if node is not None:
#                 node_id = str(node.key)
#                 dot.node(node_id, label=str(node.key))

#                 if parent:
#                     dot.edge(parent, node_id)  # Add edge from parent to current node

#                 add_edges(node.left, parent=node_id)
#                 add_edges(node.right, parent=node_id)

#         add_edges(tree.root)  # Start visualizing from the root

#     elif tree_type == "Array":
#         # Handle array-based AVL tree visualization
#         def add_edges_from_array(array, pos_x=0, parent=None):
#             """
#             Recursively add edges based on the array representation of the AVL tree.
#             `array` is the list representing the tree.
#             `parent` is the parent node for connecting edges.
#             """
#             if pos_x >= len(array) or array[pos_x] is None:
#                 return
#             node_id = str(array[pos_x])
#             dot.node(node_id, label=str(array[pos_x]))

#             if parent:
#                 dot.edge(parent, node_id)  # Add edge from parent to current node

#             # Left and right children in the array
#             left_pos_x = 2 * pos_x + 1
#             right_pos_x = 2 * pos_x + 2
#             add_edges_from_array(array, pos_x=left_pos_x, parent=node_id)
#             add_edges_from_array(array, pos_x=right_pos_x, parent=node_id)

#         add_edges_from_array(tree.tree)  # Make sure you're using `tree.tree` if that is how you're storing it

#     # Ensure the output directory exists
#     output_dir = r"C:\Users\brike\Desktop\Algoritma\visual"
#     os.makedirs(output_dir, exist_ok=True)

#     # Generate a unique filename with tree type, operation, and database size
#     output_path = get_unique_filename(output_dir, tree_type, operation, ".png")

#     # Render the visualization to the specified file path (without the extension, as Graphviz will append '.png')
#     render_with_timeout(dot, output_path)


# def get_unique_filename(folder, tree_type, operation, extension):
#     """
#     Generate a unique filename in the specified folder with tree type, operation, and database size.
#     """
#     counter = 1
#     while True:
#         filename = f"{tree_type}_{operation}_{counter}{extension}"
#         full_path = os.path.join(folder, filename)
#         if not os.path.exists(full_path):
#             return full_path
#         counter += 1


# def render_with_timeout(dot, output_path, timeout=60):
#     try:
#         # Render using Graphviz
#         dot.render(output_path[:-4], format='png', cleanup=True)
#         print(f"Tree visualization saved at {output_path}")
#     except subprocess.TimeoutExpired:
#         print("Rendering timed out.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error in rendering: {e}")