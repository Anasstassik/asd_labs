import tkinter as tk
import math
import random
from datetime import datetime
from collections import deque

VARIANT_N1N2N3N4 = 4310
N_STR = str(VARIANT_N1N2N3N4).zfill(4)
N3 = int(N_STR[2])
N4 = int(N_STR[3])
K_COEFFICIENT = 1.0 - N3 * 0.01 - N4 * 0.005 - 0.15

N_VERTICES = 11
CIRCLE_RADIUS = 225
VERTEX_SIZE = 16

BASE_CANVAS_HEIGHT = 580
UI_AREA_HEIGHT = 120
WINDOW_WIDTH_LR5 = 700
WINDOW_HEIGHT_LR5 = BASE_CANVAS_HEIGHT + UI_AREA_HEIGHT

WINDOW_CENTER_X_LR5 = WINDOW_WIDTH_LR5 // 2
WINDOW_CENTER_Y_LR5 = BASE_CANVAS_HEIGHT // 2 + 20

COLOR_DEFAULT_NODE = "lightblue"
COLOR_DISCOVERED_NODE = "yellow"
COLOR_PROCESSING_NODE = "orange"
COLOR_VISITED_NODE = "lightgreen"
COLOR_DEFAULT_EDGE = "blue"
COLOR_TREE_EDGE = "red"


def create_directed_graph_matrix(vertex_count, coefficient_k, seed_val):
    print(f"--- Генерація матриці (варіант {seed_val}) ---")
    print(f"K = {coefficient_k:.4f}")
    random.seed(seed_val)
    adjacency_matrix = []
    for _ in range(vertex_count):
        current_row = []
        for _ in range(vertex_count):
            random_value_raw = random.uniform(0.0, 2.0)
            value_with_k = random_value_raw * coefficient_k
            edge_exists = 1 if value_with_k >= 1.0 else 0
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
    print(f"\n--- {description} ---")
    if not matrix or not matrix[0] or any(row is None for row in matrix) or \
            any(any(cell is None for cell in row) for row in matrix if row):
        print("Матриця порожня або містить некоректні дані.")
        return

    num_rows = len(matrix)
    num_cols = len(matrix[0])
    print(f"Розмірність: {num_rows}x{num_cols}")

    row_num_width = len(str(num_rows))
    header_cols = " ".join(f"{j + 1:<{max(2, len(str(j + 1)))}}" for j in range(num_cols))
    header_line = " " * (row_num_width + 3) + header_cols
    print(header_line)
    separator_line = " " * row_num_width + "   " + "-" * len(header_cols)
    print(separator_line)
    for i, row_data in enumerate(matrix):
        row_str = f"{i + 1:<{row_num_width}d} | " + " ".join(
            f"{value:<{max(2, len(str(value)))}}" for value in row_data)
        print(row_str)


def draw_arrow(canvas, x1, y1, x2, y2, arrow_size=10, color="blue", offset=0):
    angle = math.atan2(y2 - y1, x2 - x1)
    _x1, _y1, _x2, _y2 = x1, y1, x2, y2
    if offset != 0:
        perp_x = -math.sin(angle) * offset;
        perp_y = math.cos(angle) * offset
        _x1 += perp_x;
        _y1 += perp_y;
        _x2 += perp_x;
        _y2 += perp_y
    canvas.create_line(_x1, _y1, _x2, _y2, fill=color, width=1, tags="edge_item")
    actual_angle_for_head = math.atan2(_y2 - _y1, _x2 - _x1)
    arrow_x1_tip = _x2 - arrow_size * math.cos(actual_angle_for_head - math.pi / 6)
    arrow_y1_tip = _y2 - arrow_size * math.sin(actual_angle_for_head - math.pi / 6)
    arrow_x2_tip = _x2 - arrow_size * math.cos(actual_angle_for_head + math.pi / 6)
    arrow_y2_tip = _y2 - arrow_size * math.sin(actual_angle_for_head + math.pi / 6)
    canvas.create_line(_x2, _y2, arrow_x1_tip, arrow_y1_tip, fill=color, width=1, tags="edge_item")
    canvas.create_line(_x2, _y2, arrow_x2_tip, arrow_y2_tip, fill=color, width=1, tags="edge_item")


def draw_self_loop(canvas, x, y, angle, loop_radius=45, arrow_size=10, color="blue"):
    start_x = x + VERTEX_SIZE * math.cos(angle);
    start_y = y + VERTEX_SIZE * math.sin(angle)
    control_point1_x = x + loop_radius * math.cos(angle - 0.3);
    control_point1_y = y + loop_radius * math.sin(angle - 0.3)
    control_point2_x = x + loop_radius * math.cos(angle + 0.8);
    control_point2_y = y + loop_radius * math.sin(angle + 0.8)
    end_angle_rad = angle + 0.6;
    end_x = x + VERTEX_SIZE * math.cos(end_angle_rad);
    end_y = y + VERTEX_SIZE * math.sin(end_angle_rad)
    canvas.create_line(start_x, start_y, control_point1_x, control_point1_y, control_point2_x, control_point2_y, end_x,
                       end_y, smooth=True, fill=color, width=1, tags="edge_item")
    arrow_head_angle = math.atan2(end_y - control_point2_y, end_x - control_point2_x)
    arrow_x1_tip = end_x - arrow_size * math.cos(arrow_head_angle - math.pi / 6);
    arrow_y1_tip = end_y - arrow_size * math.sin(arrow_head_angle - math.pi / 6)
    arrow_x2_tip = end_x - arrow_size * math.cos(arrow_head_angle + math.pi / 6);
    arrow_y2_tip = end_y - arrow_size * math.sin(arrow_head_angle + math.pi / 6)
    canvas.create_line(end_x, end_y, arrow_x1_tip, arrow_y1_tip, fill=color, width=1, tags="edge_item")
    canvas.create_line(end_x, end_y, arrow_x2_tip, arrow_y2_tip, fill=color, width=1, tags="edge_item")


def visualize_directed_graph(canvas, vertex_count, adjacency_matrix, node_colors_override=None,
                             edge_colors_override=None):
    if node_colors_override is None: node_colors_override = [COLOR_DEFAULT_NODE] * vertex_count
    if edge_colors_override is None: edge_colors_override = {}
    vertex_positions = calculate_vertex_positions(CIRCLE_RADIUS, vertex_count, WINDOW_CENTER_X_LR5, WINDOW_CENTER_Y_LR5)
    bidirectional_edges_set = set()
    if adjacency_matrix and len(adjacency_matrix) == vertex_count and all(
            len(row) == vertex_count for row in adjacency_matrix):
        for i_be in range(vertex_count):
            for j_be in range(vertex_count):
                if i_be != j_be and adjacency_matrix[i_be][j_be] == 1 and adjacency_matrix[j_be][i_be] == 1:
                    bidirectional_edges_set.add((min(i_be, j_be), max(i_be, j_be)))
    if adjacency_matrix and len(adjacency_matrix) == vertex_count:
        for i_from in range(vertex_count):
            if len(adjacency_matrix[i_from]) == vertex_count:
                for j_to in range(vertex_count):
                    if adjacency_matrix[i_from][j_to] == 1:
                        edge_current_color = edge_colors_override.get((i_from, j_to), COLOR_DEFAULT_EDGE)
                        if i_from == j_to:
                            x_loop, y_loop = vertex_positions[i_from];
                            angle_loop = -math.pi / 2 + 2 * math.pi * i_from / vertex_count
                            draw_self_loop(canvas, x_loop, y_loop, angle_loop, color=edge_current_color)
                        else:
                            x1_center, y1_center = vertex_positions[i_from];
                            x2_center, y2_center = vertex_positions[j_to]
                            delta_x = x2_center - x1_center;
                            delta_y = y2_center - y1_center
                            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
                            if distance == 0: continue
                            start_x_edge = x1_center + VERTEX_SIZE * delta_x / distance;
                            start_y_edge = y1_center + VERTEX_SIZE * delta_y / distance
                            end_x_edge = x2_center - VERTEX_SIZE * delta_x / distance;
                            end_y_edge = y2_center - VERTEX_SIZE * delta_y / distance
                            is_bidirectional_flag = (min(i_from, j_to), max(i_from, j_to)) in bidirectional_edges_set
                            current_offset_val = 8 if is_bidirectional_flag else 0
                            draw_arrow(canvas, start_x_edge, start_y_edge, end_x_edge, end_y_edge,
                                       color=edge_current_color, offset=current_offset_val)
    for i_vtx, (x_vtx, y_vtx) in enumerate(vertex_positions):
        canvas.create_oval(x_vtx - VERTEX_SIZE, y_vtx - VERTEX_SIZE, x_vtx + VERTEX_SIZE, y_vtx + VERTEX_SIZE,
                           fill=node_colors_override[i_vtx], outline="navy", tags=f"node_{i_vtx}")
        canvas.create_text(x_vtx, y_vtx, text=str(i_vtx + 1), fill="black", font=("Arial", 10, "bold"))


class GraphApp:
    def __init__(self, master_window, adj_matrix_data):
        self.master = master_window
        self.adj_matrix = adj_matrix_data
        self.num_vertices = len(adj_matrix_data)
        self.node_colors = [COLOR_DEFAULT_NODE] * self.num_vertices
        self.tree_edges = set()
        self.visited_globally = [False] * self.num_vertices
        self.current_traversal_gen = None
        self.active_traversal_name = None

        self.discovery_order_list = []
        self.node_new_numbering = {}

        self.setup_gui()
        self.redraw_graph_canvas()

    def setup_gui(self):
        self.master.title(f"ЛР5 Обхід графа - Варіант {VARIANT_N1N2N3N4}")
        info_frame = tk.Frame(self.master);
        info_frame.pack(fill=tk.X, pady=5)
        tk.Label(info_frame, text=f"Варіант: {VARIANT_N1N2N3N4}").pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text=f"Дата: {datetime.now().strftime('%d.%m.%Y')}").pack(side=tk.RIGHT, padx=10)
        controls_frame = tk.Frame(self.master);
        controls_frame.pack(fill=tk.X, pady=5)
        self.bfs_button = tk.Button(controls_frame, text="BFS Start", command=self.start_bfs);
        self.bfs_button.pack(side=tk.LEFT, padx=5)
        self.dfs_button = tk.Button(controls_frame, text="DFS Start", command=self.start_dfs);
        self.dfs_button.pack(side=tk.LEFT, padx=5)
        self.next_step_button = tk.Button(controls_frame, text="Next Step (Space)", command=self.execute_next_step,
                                          state=tk.DISABLED);
        self.next_step_button.pack(side=tk.LEFT, padx=5)
        self.reset_button = tk.Button(controls_frame, text="Reset", command=self.reset_traversal_state);
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.graph_canvas = tk.Canvas(self.master, width=WINDOW_WIDTH_LR5, height=BASE_CANVAS_HEIGHT, bg="white",
                                      borderwidth=1, relief="solid");
        self.graph_canvas.pack(padx=10, pady=5)
        protocol_area_frame = tk.Frame(self.master);
        protocol_area_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status_label = tk.Label(protocol_area_frame, text="Статус: Готовий", anchor="w")
        self.status_label.pack(fill=tk.X)

        self.protocol_text_widget = tk.Text(protocol_area_frame, height=6, relief="solid",
                                            borderwidth=1)
        self.protocol_text_widget.pack(fill=tk.BOTH, expand=True)
        self.master.bind('<space>', lambda event: self.execute_next_step_if_active())

    def execute_next_step_if_active(self):
        if self.next_step_button['state'] == tk.NORMAL: self.execute_next_step()

    def add_to_protocol(self, message):
        self.protocol_text_widget.insert(tk.END, message + "\n");
        self.protocol_text_widget.see(tk.END)

    def update_status_message(self, message):
        self.status_label.config(text=f"Статус: {message}")

    def redraw_graph_canvas(self):
        self.graph_canvas.delete("all")
        self.graph_canvas.create_text(WINDOW_WIDTH_LR5 / 2, 20,
                                      text=f"Напрямлений граф (Обхід: {self.active_traversal_name or 'немає'})",
                                      font=("Arial", 14, "bold"))
        current_edge_colors = {}
        for u_edge, v_edge in self.tree_edges: current_edge_colors[(u_edge, v_edge)] = COLOR_TREE_EDGE
        visualize_directed_graph(self.graph_canvas, self.num_vertices, self.adj_matrix,
                                 node_colors_override=self.node_colors, edge_colors_override=current_edge_colors)

    def find_start_node_for_traversal(self, for_new_component=False):
        for i in range(self.num_vertices):
            has_outgoing = any(self.adj_matrix[i][j] == 1 for j in range(self.num_vertices))
            if has_outgoing:
                if for_new_component:
                    if not self.visited_globally[i]: return i
                else:
                    return i
        return -1

    def reset_traversal_state(self):
        current_protocol_content = self.protocol_text_widget.get('1.0', tk.END)
        if "--- Скидання стану обходу ---" not in current_protocol_content.splitlines()[
                                                  -2:]:
            self.protocol_text_widget.delete('1.0', tk.END)
            self.add_to_protocol("--- Скидання стану обходу ---")

        self.node_colors = [COLOR_DEFAULT_NODE] * self.num_vertices
        self.tree_edges.clear()
        self.visited_globally = [False] * self.num_vertices
        self.discovery_order_list = []
        self.node_new_numbering = {}
        if self.current_traversal_gen:
            try:
                self.current_traversal_gen.close()
            except GeneratorExit:
                pass
            self.current_traversal_gen = None
        self.active_traversal_name = None
        self.bfs_button.config(state=tk.NORMAL);
        self.dfs_button.config(state=tk.NORMAL)
        self.next_step_button.config(state=tk.DISABLED)
        self.update_status_message("Готовий до нового обходу")
        self.redraw_graph_canvas()

    def _init_traversal(self, traversal_name, generator_func):
        self.protocol_text_widget.delete('1.0', tk.END)
        self.reset_traversal_state()
        self.active_traversal_name = traversal_name
        self.add_to_protocol(f"--- Розпочато {traversal_name} ---")
        self.update_status_message(f"{traversal_name}: Пошук стартової вершини...")
        start_node = self.find_start_node_for_traversal()
        if start_node == -1:
            msg = f"{traversal_name}: Немає вершин з вихідними дугами для початку."
            self.add_to_protocol(msg);
            self.update_status_message(msg)
            self.active_traversal_name = None;
            return False
        self.add_to_protocol(f"{traversal_name}: Старт з вершини {start_node + 1}.")
        self.current_traversal_gen = generator_func(start_node)
        self.bfs_button.config(state=tk.DISABLED);
        self.dfs_button.config(state=tk.DISABLED)
        self.next_step_button.config(state=tk.NORMAL)
        self.update_status_message(f"{traversal_name}: Готовий до 1-го кроку (з в {start_node + 1}).")
        return True

    def start_bfs(self):
        if self._init_traversal("BFS", self._bfs_step_generator): self.execute_next_step()

    def start_dfs(self):
        if self._init_traversal("DFS", self._dfs_step_generator): self.execute_next_step()

    def execute_next_step(self):
        if not self.current_traversal_gen:
            self.update_status_message("Обхід не активний.");
            self.next_step_button.config(state=tk.DISABLED)
            return
        try:
            step_details = next(self.current_traversal_gen)
            self.process_traversal_step(step_details)
        except StopIteration:
            self.add_to_protocol(f"{self.active_traversal_name}: Компонента завершена.")
            next_start_node_component = self.find_start_node_for_traversal(for_new_component=True)
            if next_start_node_component != -1:
                self.add_to_protocol(
                    f"{self.active_traversal_name}: Початок нової компоненти з в {next_start_node_component + 1}.")
                if self.active_traversal_name == "BFS":
                    self.current_traversal_gen = self._bfs_step_generator(next_start_node_component)
                else:
                    self.current_traversal_gen = self._dfs_step_generator(next_start_node_component)
                self.execute_next_step();
                return
            else:
                self.add_to_protocol(f"{self.active_traversal_name}: Обхід повністю завершено.")
                self.update_status_message(f"{self.active_traversal_name}: Завершено.")
                self.next_step_button.config(state=tk.DISABLED)
                self.bfs_button.config(state=tk.NORMAL);
                self.dfs_button.config(state=tk.NORMAL)

                traversal_tree_matrix = self.get_traversal_tree_adj_matrix()
                display_matrix(traversal_tree_matrix,
                               f"Матриця дерева обходу ({self.active_traversal_name})")

                self.display_new_numbering()

                if self.current_traversal_gen: self.current_traversal_gen.close()
                self.current_traversal_gen = None
        self.redraw_graph_canvas()

    def process_traversal_step(self, details):
        step_type = details.get('type');
        node = details.get('node');
        parent = details.get('parent')
        log_msg = f"{self.active_traversal_name}: "
        if step_type == 'start_component':
            self.node_colors[node] = COLOR_DISCOVERED_NODE
            log_msg += f"Старт компоненти з в {node + 1}."
            if node not in self.node_new_numbering:
                self.discovery_order_list.append(node)
                self.node_new_numbering[node] = len(self.discovery_order_list)
        elif step_type == 'discover':
            self.node_colors[node] = COLOR_DISCOVERED_NODE
            log_msg += f"Виявлено в {node + 1}"
            if parent is not None:
                self.tree_edges.add((parent, node))
                log_msg += f" з в {parent + 1}. Ребро ({parent + 1}-{node + 1}) - дерево."
            else:
                log_msg += "."
        elif step_type == 'process_start':
            self.node_colors[node] = COLOR_PROCESSING_NODE
            log_msg += f"Обробка в {node + 1}."
        elif step_type == 'process_finish':
            self.node_colors[node] = COLOR_VISITED_NODE
            log_msg += f"Завершено обробку в {node + 1}."
        elif step_type == 'already_known':
            log_msg += f"З в {parent + 1}: сусід в {node + 1} вже відомий."
        self.add_to_protocol(log_msg);
        self.update_status_message(log_msg)

    def _bfs_step_generator(self, start_node_idx):
        q = deque()
        yield {'type': 'start_component', 'node': start_node_idx}
        self.visited_globally[start_node_idx] = True
        q.append(start_node_idx)
        yield {'type': 'discover', 'node': start_node_idx, 'parent': None}
        while q:
            u = q.popleft()
            yield {'type': 'process_start', 'node': u}
            for v in range(self.num_vertices):
                if self.adj_matrix[u][v] == 1:
                    if not self.visited_globally[v]:
                        self.visited_globally[v] = True
                        if v not in self.node_new_numbering:
                            self.discovery_order_list.append(v)
                            self.node_new_numbering[v] = len(self.discovery_order_list)
                        q.append(v)
                        yield {'type': 'discover', 'node': v, 'parent': u}
                    else:
                        yield {'type': 'already_known', 'parent': u, 'node': v}
            yield {'type': 'process_finish', 'node': u}

    def _dfs_step_generator(self, start_node_idx):
        stack = []
        yield {'type': 'start_component', 'node': start_node_idx}
        self.visited_globally[start_node_idx] = True
        yield {'type': 'discover', 'node': start_node_idx, 'parent': None}
        stack.append((start_node_idx, iter(range(self.num_vertices))))
        yield {'type': 'process_start', 'node': start_node_idx}
        while stack:
            u, neighbors_iterator = stack[-1]
            found_unvisited_child = False
            for v in neighbors_iterator:
                if self.adj_matrix[u][v] == 1:
                    if not self.visited_globally[v]:
                        self.visited_globally[v] = True
                        if v not in self.node_new_numbering:
                            self.discovery_order_list.append(v)
                            self.node_new_numbering[v] = len(self.discovery_order_list)
                        yield {'type': 'discover', 'node': v, 'parent': u}
                        stack.append((v, iter(range(self.num_vertices))))
                        yield {'type': 'process_start', 'node': v}
                        found_unvisited_child = True;
                        break
                    else:
                        yield {'type': 'already_known', 'parent': u, 'node': v}
            if not found_unvisited_child:
                stack.pop();
                yield {'type': 'process_finish', 'node': u}

    def get_traversal_tree_adj_matrix(self):
        tree_adj_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        if not self.tree_edges and not any(self.visited_globally):
            return tree_adj_matrix
        for u_node, v_node in self.tree_edges:
            tree_adj_matrix[u_node][v_node] = 1
        return tree_adj_matrix

    def display_new_numbering(self):
        title = f"Список (вектор) відповідності номерів вершин ({self.active_traversal_name} - порядок відкриття)"
        print(f"\n--- {title} ---")

        if not self.discovery_order_list:
            print("Вершини не були відвідані або обхід не проводився.")
            return

        for new_order_idx, original_vertex_idx in enumerate(self.discovery_order_list):
            print(f"Вершина {original_vertex_idx + 1} (стара нумерація) -> Нова нумерація {new_order_idx + 1}")


def main():
    directed_matrix = create_directed_graph_matrix(N_VERTICES, K_COEFFICIENT, VARIANT_N1N2N3N4)
    display_matrix(directed_matrix, "Напрямлений граф (початковий)")

    root = tk.Tk()
    app = GraphApp(root, directed_matrix)
    root.mainloop()


if __name__ == "__main__":
    main()