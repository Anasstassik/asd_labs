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


def draw_arrow(canvas, x1, y1, x2, y2, arrow_size=10, color="blue", offset=0):
    angle = math.atan2(y2 - y1, x2 - x1)

    if offset != 0:
        perp_x = -math.sin(angle) * offset
        perp_y = math.cos(angle) * offset

        x1 += perp_x
        y1 += perp_y
        x2 += perp_x
        y2 += perp_y

    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi / 6)
    arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi / 6)
    arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi / 6)
    arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi / 6)

    canvas.create_line(x2, y2, arrow_x1, arrow_y1, fill=color, width=1)
    canvas.create_line(x2, y2, arrow_x2, arrow_y2, fill=color, width=1)


def draw_self_loop(canvas, x, y, angle, loop_radius=45, arrow_size=10):
    start_x = x + VERTEX_SIZE * math.cos(angle)
    start_y = y + VERTEX_SIZE * math.sin(angle)

    control_point1_x = x + loop_radius * math.cos(angle - 0.3)
    control_point1_y = y + loop_radius * math.sin(angle - 0.3)

    control_point2_x = x + loop_radius * math.cos(angle + 0.8)
    control_point2_y = y + loop_radius * math.sin(angle + 0.8)

    end_angle = angle + 0.6
    end_x = x + VERTEX_SIZE * math.cos(end_angle)
    end_y = y + VERTEX_SIZE * math.sin(end_angle)

    canvas.create_line(start_x, start_y,
                       control_point1_x, control_point1_y,
                       control_point2_x, control_point2_y,
                       end_x, end_y,
                       smooth=True, fill="blue", width=1)

    arrow_point_x = end_x - 2 * math.cos(end_angle)
    arrow_point_y = end_y - 2 * math.sin(end_angle)

    arrow_angle = math.atan2(end_y - control_point2_y, end_x - control_point2_x)

    arrow_x1 = arrow_point_x - arrow_size * math.cos(arrow_angle - math.pi / 6)
    arrow_y1 = arrow_point_y - arrow_size * math.sin(arrow_angle - math.pi / 6)
    arrow_x2 = arrow_point_x - arrow_size * math.cos(arrow_angle + math.pi / 6)
    arrow_y2 = arrow_point_y - arrow_size * math.sin(arrow_angle + math.pi / 6)

    canvas.create_line(end_x, end_y, arrow_x1, arrow_y1, fill="blue", width=1)
    canvas.create_line(end_x, end_y, arrow_x2, arrow_y2, fill="blue", width=1)


def visualize_directed_graph(canvas, vertex_count, adjacency_matrix):
    vertex_positions = calculate_vertex_positions(CIRCLE_RADIUS, vertex_count,
                                                  WINDOW_CENTER_X, WINDOW_CENTER_Y)

    bidirectional_edges = set()

    for i in range(vertex_count):
        for j in range(vertex_count):
            if i != j and adjacency_matrix[i][j] == 1 and adjacency_matrix[j][i] == 1:
                if i < j:
                    bidirectional_edges.add((i, j))
                else:
                    bidirectional_edges.add((j, i))

    for i in range(vertex_count):
        for j in range(vertex_count):
            if adjacency_matrix[i][j] == 1:
                if i == j:
                    x, y = vertex_positions[i]
                    angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
                    draw_self_loop(canvas, x, y, angle)
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

                    is_bidirectional = (min(i, j), max(i, j)) in bidirectional_edges

                    if is_bidirectional:
                        offset = 8
                        draw_arrow(canvas, start_x, start_y, end_x, end_y, offset=offset)
                    else:
                        draw_arrow(canvas, start_x, start_y, end_x, end_y)

    for i, (x, y) in enumerate(vertex_positions):
        canvas.create_oval(x - VERTEX_SIZE, y - VERTEX_SIZE,
                           x + VERTEX_SIZE, y + VERTEX_SIZE,
                           fill="lightblue", outline="navy")

        canvas.create_text(x, y, text=str(i + 1),
                           fill="black", font=("Arial", 10, "bold"))


def main():
    directed_matrix = create_directed_graph_matrix(N, K, SEED)

    display_matrix(directed_matrix, f"Орієнтований граф (вершин: {N})")

    root = tk.Tk()
    root.title(f"Журавель Анастасія, варіант: {SEED} - Напрямлений граф")

    current_date = datetime.now().strftime("%d.%m.%Y")
    version_label = tk.Label(root, text=f"Версія програми: 2.1 (від {current_date})")
    version_label.pack(pady=5)

    graph_canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                             bg="white", borderwidth=1, relief="solid")
    graph_canvas.pack(padx=10, pady=5)

    graph_canvas.create_text(WINDOW_WIDTH / 2, 20,
                             text="Напрямлений граф",
                             font=("Arial", 14, "bold"))

    visualize_directed_graph(graph_canvas, N, directed_matrix)

    root.mainloop()


if __name__ == "__main__":
    main()