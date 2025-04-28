import tkinter as tk
import math
import random
from datetime import datetime

SEED = 4310
N = 11
K = 1.0 - 0.02 - 0.00 - 0.25 - 0.01 + 0.01
CIRCLE_RADIUS = 225
VERTEX_SIZE = 16
WINDOW_WIDTH = 610
WINDOW_HEIGHT = 630
WINDOW_CENTER_X = WINDOW_WIDTH // 2
WINDOW_CENTER_Y = WINDOW_HEIGHT // 2 + 20


def create_directed_graph_matrix(vertex_count, coefficient, random_seed):
    random.seed(random_seed)

    adjacency_matrix = []
    for row_index in range(vertex_count):
        current_row = []
        for col_index in range(vertex_count):
            random_value = random.uniform(0.1, 2.1) * coefficient
            edge_exists = 1 if random_value >= 1.1 else 0
            current_row.append(edge_exists)
        adjacency_matrix.append(current_row)

    return adjacency_matrix


def convert_to_undirected_graph(directed_matrix):
    size = len(directed_matrix)
    undirected_matrix = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if directed_matrix[i][j] == 1 or directed_matrix[j][i] == 1:
                undirected_matrix[i][j] = 1
                undirected_matrix[j][i] = 1

    return undirected_matrix


def calculate_vertex_positions(radius, vertex_count, center_x, center_y):
    vertex_positions = []

    for i in range(vertex_count):
        angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
        x_coord = center_x + radius * math.cos(angle)
        y_coord = center_y + radius * math.sin(angle)
        vertex_positions.append((x_coord, y_coord))

    return vertex_positions


def display_matrix(matrix, description="Матриця графа"):
    print(f"\n=== {description} ===")
    print(f"Розмірність: {len(matrix)}x{len(matrix[0])}")

    header = "    " + " ".join(f"{i + 1:2d}" for i in range(len(matrix)))
    print(header)
    print("   " + "-" * (len(header) - 3))

    for i, row in enumerate(matrix):
        row_str = " ".join(f"{value:2d}" for value in row)
        print(f"{i + 1:2d} | {row_str}")


def visualize_graph(canvas, vertex_count, adjacency_matrix):
    vertex_positions = calculate_vertex_positions(CIRCLE_RADIUS, vertex_count,
                                                  WINDOW_CENTER_X, WINDOW_CENTER_Y)

    for i in range(vertex_count):
        for j in range(i + 1):
            if adjacency_matrix[i][j] == 1:
                if i == j:
                    x, y = vertex_positions[i]

                    angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
                    loop_radius = 45

                    start_x = x + VERTEX_SIZE * math.cos(angle)
                    start_y = y + VERTEX_SIZE * math.sin(angle)

                    control_point1_x = x + loop_radius * math.cos(angle - 0.1)
                    control_point1_y = y + loop_radius * math.sin(angle - 0.1)

                    control_point2_x = x + loop_radius * math.cos(angle + 0.8)
                    control_point2_y = y + loop_radius * math.sin(angle + 0.8)

                    end_x = x + VERTEX_SIZE * math.cos(angle + 0.6)
                    end_y = y + VERTEX_SIZE * math.sin(angle + 0.6)

                    canvas.create_line(start_x, start_y,
                                       control_point1_x, control_point1_y,
                                       control_point2_x, control_point2_y,
                                       end_x, end_y,
                                       smooth=True, fill="blue", width=1)
                else:
                    x1, y1 = vertex_positions[i]
                    x2, y2 = vertex_positions[j]

                    delta_x = x2 - x1
                    delta_y = y2 - y1
                    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

                    start_x = x1 + VERTEX_SIZE * delta_x / distance
                    start_y = y1 + VERTEX_SIZE * delta_y / distance
                    end_x = x2 - VERTEX_SIZE * delta_x / distance
                    end_y = y2 - VERTEX_SIZE * delta_y / distance

                    canvas.create_line(start_x, start_y, end_x, end_y,
                                       fill="blue", width=1)

    for i, (x, y) in enumerate(vertex_positions):
        canvas.create_oval(x - VERTEX_SIZE, y - VERTEX_SIZE,
                           x + VERTEX_SIZE, y + VERTEX_SIZE,
                           fill="lightblue", outline="navy")

        canvas.create_text(x, y, text=str(i + 1),
                           fill="black", font=("Arial", 10, "bold"))


def main():
    directed_matrix = create_directed_graph_matrix(N, K, SEED)
    undirected_matrix = convert_to_undirected_graph(directed_matrix)

    display_matrix(directed_matrix, f"Орієнтований граф (вершин: {N})")
    display_matrix(undirected_matrix, f"Неорієнтований граф (вершин: {N})")

    root = tk.Tk()
    root.title(f"Журавель Анастасія, варіант: {SEED} - Ненапрямлений граф")

    current_date = datetime.now().strftime("%d.%m.%Y")
    version_label = tk.Label(root, text=f"Версія програми: 2.1 (від {current_date})")
    version_label.pack(pady=5)

    graph_canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                             bg="white", borderwidth=1, relief="solid")
    graph_canvas.pack(padx=10, pady=5)

    graph_canvas.create_text(WINDOW_WIDTH / 2, 20,
                             text="Ненапрямлений граф",
                             font=("Arial", 14, "bold"))

    visualize_graph(graph_canvas, N, undirected_matrix)

    root.mainloop()


if __name__ == "__main__":
    main()