import random

def create_directed_graph_matrix(vertex_count, k_coefficient, random_seed):
    random.seed(random_seed)
    adjacency_matrix = []
    for _ in range(vertex_count):
        current_row = []
        for _ in range(vertex_count):
            random_base_value = random.uniform(0.0, 2.0)
            multiplied_value = random_base_value * k_coefficient
            edge_exists = 1 if multiplied_value >= 1.0 else 0
            current_row.append(edge_exists)
        adjacency_matrix.append(current_row)
    return adjacency_matrix

def convert_to_undirected_graph(directed_matrix):
    size = len(directed_matrix)
    undirected_matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i, size):
            if directed_matrix[i][j] == 1 or directed_matrix[j][i] == 1:
                undirected_matrix[i][j] = 1
                undirected_matrix[j][i] = 1
    return undirected_matrix

def display_matrix(matrix, description="Матриця графа"):
    print(f"\n--- {description} ---")
    if not matrix or not matrix[0]:
        print("Матриця порожня.")
        return
    print(f"Розмірність: {len(matrix)}x{len(matrix[0])}")
    header = "    " + " ".join(f"{i + 1:2d}" for i in range(len(matrix[0])))
    print(header)
    print("   " + "-" * (len(header) - 3))
    for i, row in enumerate(matrix):
        row_str = " ".join(f"{value:2d}" for value in row)
        print(f"{i + 1:2d} | {row_str}")