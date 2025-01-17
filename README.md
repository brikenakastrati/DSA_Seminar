# AVL Tree Performance Comparison
#### This repository implements AVL trees over two types of binary trees:
#### 1.Reference-based Binary Tree: Uses class-based nodes
#### 2.Array-based Binary Tree: Uses arrays to represent the binary tree structure.

#### The project compares time and memory complexities of AVL tree operations (insert, delete, search) on both implementations. The repository also includes datasets for experiments and visualizations of tree operations using Graphviz.

## Instructions to run the code: 
 #### 1.Clone the repository from GitHub:
     git clone https://github.com/brikenakastrati/DSA_Seminar
#### 2. Install Python
Ensure **Python 3.8 or higher** is installed on your system:
 [Download Python from the Official Website](https://www.python.org/downloads/)

 #### 3.Create and activate a virtual environment:
      python -m venv venv
      source venv/bin/activate  # On Windows: .venv\Scripts\activate
#### 4. Install Graphviz
Download and install **Graphviz** for tree visualizations:
[Graphviz Downloads and Installation Guide](https://graphviz.org/download/)

#### 5.Install the required libraries:
       pip install matplotlib
       pip install graphviz
       pip install numpy
       pip install memory-profiler

#### 6.Generate datasets by running the script:
      py datasets/generate_datasets.py

#### 7.Run benchmarks:
      py src/benchmark.py

### 8.Generate performance graphs:
     py graphs/generate_graphs.py
      
