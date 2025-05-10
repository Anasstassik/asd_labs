def calculate_undirected_degrees(adj_matrix_undir):
    n = len(adj_matrix_undir)
    degrees = [0] * n
    for i in range(n):
        current_degree = sum(adj_matrix_undir[i])
        if adj_matrix_undir[i][i] == 1:
            degrees[i] = current_degree + 1
        else:
            degrees[i] = current_degree
    return degrees

def calculate_directed_degrees(adj_matrix_dir):
    n = len(adj_matrix_dir)
    out_degrees = [sum(row) for row in adj_matrix_dir]
    in_degrees = [sum(adj_matrix_dir[k][i] for k in range(n)) for i in range(n)]
    return out_degrees, in_degrees

def check_undirected_regularity(degrees):
    if not degrees: return False, 0
    first_degree = degrees[0]
    is_regular = all(d == first_degree for d in degrees)
    return is_regular, first_degree if is_regular else 0

def check_directed_regularity(out_degrees, in_degrees):
    if not out_degrees or len(out_degrees) != len(in_degrees): return False, 0
    first_out_degree = out_degrees[0]
    if not all(d == first_out_degree for d in out_degrees): return False, 0
    first_in_degree = in_degrees[0]
    if not all(d == first_in_degree for d in in_degrees): return False, 0
    return first_out_degree == first_in_degree, first_out_degree if first_out_degree == first_in_degree else 0

def find_special_vertices_undirected(degrees):
    pendant = [i + 1 for i, degree in enumerate(degrees) if degree == 1]
    isolated = [i + 1 for i, degree in enumerate(degrees) if degree == 0]
    return pendant, isolated

def find_special_vertices_directed(out_degrees, in_degrees):
    pendant = [i + 1 for i, (o, inv) in enumerate(zip(out_degrees, in_degrees)) if o + inv == 1]
    isolated = [i + 1 for i, (o, inv) in enumerate(zip(out_degrees, in_degrees)) if o == 0 and inv == 0]
    return pendant, isolated

def find_paths_of_length(adj_matrix, length):
    n = len(adj_matrix)
    found_paths = []
    if length == 2:
        for i in range(n):
            for m in range(n):
                if adj_matrix[i][m] == 1:
                    for j in range(n):
                        if adj_matrix[m][j] == 1:
                            found_paths.append(f"{i+1} -> {m+1} -> {j+1}")
    elif length == 3:
        for i in range(n):
            for m in range(n):
                if adj_matrix[i][m] == 1:
                    for p in range(n):
                        if adj_matrix[m][p] == 1:
                            for j in range(n):
                                if adj_matrix[p][j] == 1:
                                    found_paths.append(f"{i+1} -> {m+1} -> {p+1} -> {j+1}")
    return found_paths

def warshall_reachability_matrix(adj_matrix):
    n = len(adj_matrix)
    reach_matrix = [row[:] for row in adj_matrix]
    for i in range(n):
        reach_matrix[i][i] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach_matrix[i][k] == 1 and reach_matrix[k][j] == 1:
                    reach_matrix[i][j] = 1
    return reach_matrix

def strong_connectivity_matrix(reach_matrix):
    n = len(reach_matrix)
    scc_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if reach_matrix[i][j] == 1 and reach_matrix[j][i] == 1:
                scc_matrix[i][j] = 1
    return scc_matrix

def find_strongly_connected_components(s_conn_matrix):
    n = len(s_conn_matrix)
    sccs = []
    visited_nodes = [False] * n
    for i in range(n):
        if not visited_nodes[i]:
            current_scc = [j + 1 for j in range(n) if s_conn_matrix[i][j] == 1]
            if current_scc:
                for node_idx_plus_1 in current_scc:
                    visited_nodes[node_idx_plus_1 - 1] = True
                sccs.append(sorted(list(set(current_scc))))
    return sccs

def build_condensation_graph(original_adj_matrix, scc_list):
    num_sccs = len(scc_list)
    if num_sccs == 0: return [], []
    node_to_scc_map = {node_val - 1: scc_idx
                       for scc_idx, component_nodes in enumerate(scc_list)
                       for node_val in component_nodes}
    condensation_adj_matrix = [[0] * num_sccs for _ in range(num_sccs)]
    for u_orig in range(len(original_adj_matrix)):
        for v_orig in range(len(original_adj_matrix)):
            if original_adj_matrix[u_orig][v_orig] == 1:
                scc_u_idx = node_to_scc_map.get(u_orig)
                scc_v_idx = node_to_scc_map.get(v_orig)
                if scc_u_idx is not None and scc_v_idx is not None and scc_u_idx != scc_v_idx:
                    condensation_adj_matrix[scc_u_idx][scc_v_idx] = 1
    scc_labels_for_graph = [",".join(map(str, scc)) for scc in scc_list]
    return condensation_adj_matrix, scc_labels_for_graph