import tkinter as tk
import math
import random
from datetime import datetime

VARIANT_SEED = 4310
N1, N2, N3, N4 = 4, 3, 1, 0
NUM_VERTICES = 10 + N3
K_COEFF = 1.0 - N3 / 10.0 - 0.01 * N4 - 0.005 - 0.05

CIRCLE_RADIUS = 200
VERTEX_SIZE = 15
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
CANVAS_DRAW_HEIGHT = WINDOW_HEIGHT - 100

WINDOW_CENTER_X1 = WINDOW_WIDTH // 4
WINDOW_CENTER_Y_GRAPHS = CANVAS_DRAW_HEIGHT // 2 + 10
WINDOW_CENTER_X2 = (WINDOW_WIDTH // 4) * 3


def generate_Adir(num_vertices, k_coeff, seed):
    random.seed(seed)
    adj_matrix = []
    for _ in range(num_vertices):
        row = []
        for _ in range(num_vertices):
            val = random.uniform(0, 2.0)
            val *= k_coeff
            row.append(1 if val >= 1.0 else 0)
        adj_matrix.append(row)
    return adj_matrix


def generate_Aundir(Adir_matrix):
    num_vertices = len(Adir_matrix)
    Aundir_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                Aundir_matrix[i][j] = 0
            elif Adir_matrix[i][j] == 1 or Adir_matrix[j][i] == 1:
                Aundir_matrix[i][j] = 1
    return Aundir_matrix


def generate_W(num_vertices, seed, Aundir_matrix):
    random.seed(seed)
    B_matrix = [[random.uniform(0, 2.0) for _ in range(num_vertices)] for _ in range(num_vertices)]
    C_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            C_matrix[i][j] = math.ceil(B_matrix[i][j] * 100 * Aundir_matrix[i][j])

    D_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            D_matrix[i][j] = 1 if C_matrix[i][j] > 0 else 0

    H_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            H_matrix[i][j] = 1 if D_matrix[i][j] != D_matrix[j][i] else 0

    W_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i, num_vertices):
            d_ij = D_matrix[i][j]
            h_ij = H_matrix[i][j]
            c_ij = C_matrix[i][j]

            tr_ij = 1 if i < j else 0

            weight = (d_ij + h_ij + tr_ij) * c_ij

            W_matrix[i][j] = weight
            W_matrix[j][i] = weight

            if Aundir_matrix[i][j] == 0:
                W_matrix[i][j] = 0
                W_matrix[j][i] = 0
            elif i == j:
                W_matrix[i][j] = 0
    return W_matrix


def display_matrix(matrix, description="Матриця"):
    print(f"\n=== {description} ===")
    if not matrix or not matrix[0]:
        print("Матриця порожня або некоректна.")
        return
    rows = len(matrix)
    cols = len(matrix[0])
    print(f"Розмірність: {rows}x{cols}")
    header = "    " + " ".join(f"{idx + 1:3d}" for idx in range(cols))
    print(header)
    print("   " + "-" * (len(header) - 3))
    for i, row_data in enumerate(matrix):
        row_str = " ".join(f"{value:3d}" for value in row_data)
        print(f"{i + 1:2d} | {row_str}")


class DSU:
    def __init__(self, num_vertices):
        self.parent = list(range(num_vertices))
        self.rank = [0] * num_vertices

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


class KruskalAlgorithm:
    def __init__(self, num_vertices, edges_with_weights):
        self.num_vertices = num_vertices
        self.all_edges = sorted([edge for edge in edges_with_weights if edge[0] > 0])

        self.dsu = DSU(num_vertices)
        self.mst_edges = []
        self.mst_total_weight = 0
        self.current_edge_index = 0
        self.last_considered_edge = None

    def step(self):
        if self.is_done():
            self.last_considered_edge = None
            return False

        weight, u, v = self.all_edges[self.current_edge_index]

        print(f"Розглядається ребро ({u + 1}-{v + 1}) з вагою {weight}.")

        if self.dsu.find(u) != self.dsu.find(v):
            if self.dsu.union(u, v):
                self.mst_edges.append((u, v, weight))
                self.mst_total_weight += weight
                self.last_considered_edge = (u, v, weight, 'added')
                print(f"  -> ДОДАНО. Нова вага MST: {self.mst_total_weight}")
        else:
            self.last_considered_edge = (u, v, weight, 'rejected')
            print(f"  -> ВІДХИЛЕНО (утворює цикл).")

        self.current_edge_index += 1
        return True

    def is_done(self):
        if self.num_vertices == 0:
            return self.current_edge_index >= len(self.all_edges)
        if self.current_edge_index >= len(self.all_edges):
            return True
        if len(self.mst_edges) == self.num_vertices - 1:
            return True
        return False


def calculate_vertex_positions(radius, vertex_count, center_x, center_y):
    positions = []
    for i in range(vertex_count):
        angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions.append((x, y))
    return positions


def draw_edge(canvas, x1, y1, x2, y2, weight, color="gray", width=1, text_color="black"):
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width, tags="edge_line")
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0: return

    offset = 10
    text_x = mid_x + offset * dy / dist
    text_y = mid_y - offset * dx / dist

    canvas.create_text(text_x, text_y, text=str(weight), fill=text_color, font=("Arial", 8), tags="edge_weight")


class GraphVisualizerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title(f"Журавель Анастасія, варіант: {VARIANT_SEED} - MST (Краскал)")

        self.Adir = generate_Adir(NUM_VERTICES, K_COEFF, VARIANT_SEED)
        self.Aundir = generate_Aundir(self.Adir)
        self.W = generate_W(NUM_VERTICES, VARIANT_SEED, self.Aundir)

        display_matrix(self.Adir, "Adir - Орієнтований граф")
        display_matrix(self.Aundir, "Aundir - Неорієнтований граф")
        display_matrix(self.W, "W - Матриця ваг")

        self.vertex_pos = calculate_vertex_positions(CIRCLE_RADIUS, NUM_VERTICES,
                                                     WINDOW_CENTER_X1, WINDOW_CENTER_Y_GRAPHS)
        self.mst_vertex_pos = calculate_vertex_positions(CIRCLE_RADIUS, NUM_VERTICES,
                                                         WINDOW_CENTER_X2, WINDOW_CENTER_Y_GRAPHS)

        self.all_graph_edges_from_W = []
        for i in range(NUM_VERTICES):
            for j in range(i + 1, NUM_VERTICES):
                if self.Aundir[i][j] == 1:
                    self.all_graph_edges_from_W.append((self.W[i][j], i, j))

        self.kruskal_algo = KruskalAlgorithm(NUM_VERTICES, self.all_graph_edges_from_W)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        self.next_step_button = tk.Button(self.controls_frame, text="Наступний крок (Пробіл)",
                                          command=self.perform_step)
        self.next_step_button.pack(side=tk.LEFT, padx=5)

        self.run_all_button = tk.Button(self.controls_frame, text="Виконати все", command=self.run_all_steps)
        self.run_all_button.pack(side=tk.LEFT, padx=5)

        self.text_y_offset_from_bottom = 25

        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=CANVAS_DRAW_HEIGHT, bg="white", borderwidth=1,
                                relief="solid")
        self.canvas.pack(padx=10, pady=5)

        self.root.bind('<space>', lambda event: self.perform_step())

        self.draw_initial_state()

        has_positive_weight_edges = any(edge[0] > 0 for edge in self.kruskal_algo.all_edges)

        if NUM_VERTICES == 0:
            message = "УВАГА: Граф не має вершин."
            print(f"\n{message} MST не може бути побудовано.")
            self.next_step_button.config(state=tk.DISABLED)
            self.run_all_button.config(state=tk.DISABLED)
        elif not has_positive_weight_edges and NUM_VERTICES > 0:
            message = "УВАГА: Граф не має ребер з позитивною вагою."
            print(f"\n{message} MST не може бути побудовано.")
            self.next_step_button.config(state=tk.DISABLED)
            self.run_all_button.config(state=tk.DISABLED)

    def draw_initial_state(self):
        self.canvas.delete("all")
        self.canvas.create_text(WINDOW_CENTER_X1, 20, text="Початковий граф", font=("Arial", 14, "bold"))
        self.canvas.create_text(WINDOW_CENTER_X2, 20, text="Мінімальний остов (MST)", font=("Arial", 14, "bold"))
        self.canvas.create_line(WINDOW_WIDTH / 2, 0, WINDOW_WIDTH / 2, CANVAS_DRAW_HEIGHT, fill="lightgray")

        for i in range(NUM_VERTICES):
            x1, y1 = self.vertex_pos[i]
            self.canvas.create_oval(x1 - VERTEX_SIZE, y1 - VERTEX_SIZE, x1 + VERTEX_SIZE, y1 + VERTEX_SIZE,
                                    fill="lightblue", outline="navy", tags=f"v_orig_{i}")
            self.canvas.create_text(x1, y1, text=str(i + 1), fill="black", font=("Arial", 10, "bold"),
                                    tags=f"vt_orig_{i}")

            x2, y2 = self.mst_vertex_pos[i]
            self.canvas.create_oval(x2 - VERTEX_SIZE, y2 - VERTEX_SIZE, x2 + VERTEX_SIZE, y2 + VERTEX_SIZE,
                                    fill="lightyellow", outline="orange", tags=f"v_mst_{i}")
            self.canvas.create_text(x2, y2, text=str(i + 1), fill="black", font=("Arial", 10, "bold"),
                                    tags=f"vt_mst_{i}")

        for weight, u, v in self.kruskal_algo.all_edges:
            x1_orig, y1_orig = self.vertex_pos[u]
            x2_orig, y2_orig = self.vertex_pos[v]
            draw_edge(self.canvas, x1_orig, y1_orig, x2_orig, y2_orig, weight, color="gray", width=1)

        y_coord_for_mst_weight = CANVAS_DRAW_HEIGHT - self.text_y_offset_from_bottom
        self.canvas.create_text(WINDOW_CENTER_X2, y_coord_for_mst_weight,
                                text=f"Вага MST: 0",
                                font=("Arial", 12, "bold"), tags="mst_weight_text")

    def perform_step(self):
        if not self.kruskal_algo.is_done():
            step_performed = self.kruskal_algo.step()
            if step_performed:
                self.update_visualization()
            if self.kruskal_algo.is_done():
                self.finalize_algorithm_display()
        else:
            self.finalize_algorithm_display(already_done=True)

    def run_all_steps(self):
        if not self.kruskal_algo.all_edges and NUM_VERTICES > 0:
            print("Неможливо виконати всі кроки: немає ребер для розгляду.")
            return
        if self.kruskal_algo.is_done():
            return

        while not self.kruskal_algo.is_done():
            self.kruskal_algo.step()

        self.update_visualization()
        self.finalize_algorithm_display()

    def finalize_algorithm_display(self, already_done=False):
        if already_done and self.next_step_button['state'] == tk.DISABLED:
            return

        print(f"\nПідсумкова вага MST: {self.kruskal_algo.mst_total_weight}")
        final_mst_edges_str = ', '.join([f"({e[0] + 1}-{e[1] + 1}, {e[2]})" for e in self.kruskal_algo.mst_edges])
        print(f"Ребра в MST: [{final_mst_edges_str if final_mst_edges_str else 'немає ребер'}]")
        print(f"Кількість ребер в MST: {len(self.kruskal_algo.mst_edges)}")

        if NUM_VERTICES > 1 and \
                len(self.kruskal_algo.mst_edges) < NUM_VERTICES - 1 and \
                self.kruskal_algo.current_edge_index >= len(self.kruskal_algo.all_edges) and \
                not already_done:
            print("УВАГА: Граф може бути незв'язним. Побудовано мінімальний остовний ліс.")

        self.next_step_button.config(state=tk.DISABLED)
        self.run_all_button.config(state=tk.DISABLED)

        self.canvas.delete("mst_weight_text")
        y_coord_for_mst_weight = CANVAS_DRAW_HEIGHT - self.text_y_offset_from_bottom
        self.canvas.create_text(WINDOW_CENTER_X2, y_coord_for_mst_weight,
                                text=f"Вага MST: {self.kruskal_algo.mst_total_weight}",
                                font=("Arial", 12, "bold"), tags="mst_weight_text")

    def update_visualization(self):
        self.canvas.delete("edge_line")
        self.canvas.delete("edge_weight")
        self.canvas.delete("mst_weight_text")

        for weight_orig, u_orig, v_orig in self.kruskal_algo.all_edges:
            x1, y1 = self.vertex_pos[u_orig]
            x2, y2 = self.vertex_pos[v_orig]
            draw_edge(self.canvas, x1, y1, x2, y2, weight_orig, color="lightgray", width=1)

        for u_mst, v_mst, w_mst in self.kruskal_algo.mst_edges:
            x1, y1 = self.vertex_pos[u_mst]
            x2, y2 = self.vertex_pos[v_mst]
            draw_edge(self.canvas, x1, y1, x2, y2, w_mst, color="green", width=2.5)

        last_edge_info = self.kruskal_algo.last_considered_edge
        if last_edge_info:
            u, v, weight, status = last_edge_info
            x1_curr, y1_curr = self.vertex_pos[u]
            x2_curr, y2_curr = self.vertex_pos[v]

            if status == 'rejected':
                draw_edge(self.canvas, x1_curr, y1_curr, x2_curr, y2_curr, weight, color="red", width=3)
            elif status == 'added' and not self.kruskal_algo.is_done():
                draw_edge(self.canvas, x1_curr, y1_curr, x2_curr, y2_curr, weight, color="lime green", width=3)

        for u_mst, v_mst, weight_mst in self.kruskal_algo.mst_edges:
            x1_mst_draw, y1_mst_draw = self.mst_vertex_pos[u_mst]
            x2_mst_draw, y2_mst_draw = self.mst_vertex_pos[v_mst]
            draw_edge(self.canvas, x1_mst_draw, y1_mst_draw, x2_mst_draw, y2_mst_draw, weight_mst, color="forestgreen",
                      width=2.5, text_color="darkgreen")

        y_coord_for_mst_weight = CANVAS_DRAW_HEIGHT - self.text_y_offset_from_bottom
        self.canvas.create_text(WINDOW_CENTER_X2, y_coord_for_mst_weight,
                                text=f"Вага MST: {self.kruskal_algo.mst_total_weight}",
                                font=("Arial", 12, "bold"), tags="mst_weight_text")


def main():
    root = tk.Tk()
    app = GraphVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()