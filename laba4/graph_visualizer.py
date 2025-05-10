import tkinter as tk
import math

DEFAULT_CIRCLE_RADIUS = 225
DEFAULT_VERTEX_SIZE = 16
DEFAULT_WINDOW_WIDTH = 610
DEFAULT_WINDOW_HEIGHT = 630
DEFAULT_LOOP_RADIUS_VIZ = 45


def calculate_vertex_positions(radius, vertex_count, center_x, center_y):
    return [(center_x + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / vertex_count),
             center_y + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / vertex_count))
            for i in range(vertex_count)]


def draw_arrow(canvas, x1, y1, x2, y2, arrow_size=10, color="blue", offset=0, line_dash=None):
    angle = math.atan2(y2 - y1, x2 - x1)
    if offset != 0:
        perp_x = -math.sin(angle) * offset;
        perp_y = math.cos(angle) * offset
        x1 += perp_x;
        y1 += perp_y;
        x2 += perp_x;
        y2 += perp_y

    line_options = {"fill": color, "width": 1.5}
    if line_dash:
        line_options["dash"] = line_dash
    canvas.create_line(x1, y1, x2, y2, **line_options)

    arrow_x1 = x2 - arrow_size * math.cos(angle - math.pi / 6)
    arrow_y1 = y2 - arrow_size * math.sin(angle - math.pi / 6)
    arrow_x2 = x2 - arrow_size * math.cos(angle + math.pi / 6)
    arrow_y2 = y2 - arrow_size * math.sin(angle + math.pi / 6)
    canvas.create_line(x2, y2, arrow_x1, arrow_y1, fill=color, width=1)
    canvas.create_line(x2, y2, arrow_x2, arrow_y2, fill=color, width=1)


def draw_self_loop(canvas, x, y, angle, loop_radius, vertex_size, arrow_size=10, color="blue", is_directed=True):
    start_x = x + vertex_size * math.cos(angle)
    start_y = y + vertex_size * math.sin(angle)
    control_point1_x = x + loop_radius * math.cos(angle - 0.3)
    control_point1_y = y + loop_radius * math.sin(angle - 0.3)
    control_point2_x = x + loop_radius * math.cos(angle + 0.8)
    control_point2_y = y + loop_radius * math.sin(angle + 0.8)
    end_angle = angle + 0.6
    end_x_loop = x + vertex_size * math.cos(end_angle if is_directed else angle + 0.1)
    end_y_loop = y + vertex_size * math.sin(end_angle if is_directed else angle + 0.1)
    canvas.create_line(start_x, start_y, control_point1_x, control_point1_y,
                       control_point2_x, control_point2_y, end_x_loop, end_y_loop,
                       smooth=True, fill=color, width=1)
    if is_directed:
        arrow_point_x = end_x_loop - 2 * math.cos(end_angle)
        arrow_point_y = end_y_loop - 2 * math.sin(end_angle)
        arrow_angle_loop = math.atan2(end_y_loop - control_point2_y, end_x_loop - control_point2_x)
        arrow_x1 = arrow_point_x - arrow_size * math.cos(arrow_angle_loop - math.pi / 6)
        arrow_y1 = arrow_point_y - arrow_size * math.sin(arrow_angle_loop - math.pi / 6)
        arrow_x2 = arrow_point_x - arrow_size * math.cos(arrow_angle_loop + math.pi / 6)
        arrow_y2 = arrow_point_y - arrow_size * math.sin(arrow_angle_loop + math.pi / 6)
        canvas.create_line(end_x_loop, end_y_loop, arrow_x1, arrow_y1, fill=color, width=1)
        canvas.create_line(end_x_loop, end_y_loop, arrow_x2, arrow_y2, fill=color, width=1)


def visualize_directed_graph_on_canvas(canvas, vertex_count, adj_matrix,
                                       circle_radius, vertex_size, window_center_x, window_center_y, loop_radius_viz,
                                       graph_color="blue", fill_color="lightblue", outline_color="navy",
                                       title_text="Напрямлений граф"):
    canvas.create_text(window_center_x, 20, text=title_text, font=("Arial", 14, "bold"))
    vertex_positions = calculate_vertex_positions(circle_radius, vertex_count, window_center_x, window_center_y)

    bidirectional_edges_map = {}
    for r in range(vertex_count):
        for c in range(vertex_count):
            if adj_matrix[r][c] == 1 and adj_matrix[c][r] == 1 and r != c:
                bidirectional_edges_map[tuple(sorted((r, c)))] = True

    for i in range(vertex_count):
        for j in range(vertex_count):
            if adj_matrix[i][j] == 1:
                x1_node, y1_node = vertex_positions[i]
                x2_node, y2_node = vertex_positions[j]

                if i == j:
                    angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
                    draw_self_loop(canvas, x1_node, y1_node, angle, loop_radius=loop_radius_viz,
                                   vertex_size=vertex_size, color=graph_color, is_directed=True)
                else:
                    delta_x = x2_node - x1_node;
                    delta_y = y2_node - y1_node
                    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
                    if distance == 0: continue

                    start_x = x1_node + vertex_size * delta_x / distance
                    start_y = y1_node + vertex_size * delta_y / distance
                    end_x = x2_node - vertex_size * delta_x / distance
                    end_y = y2_node - vertex_size * delta_y / distance

                    offset = 0
                    if tuple(sorted((i, j))) in bidirectional_edges_map and i < j:
                        offset = 8

                    draw_arrow(canvas, start_x, start_y, end_x, end_y, offset=offset, color=graph_color)

    for i, (x, y) in enumerate(vertex_positions):
        canvas.create_oval(x - vertex_size, y - vertex_size, x + vertex_size, y + vertex_size, fill=fill_color,
                           outline=outline_color)
        canvas.create_text(x, y, text=str(i + 1), fill="black", font=("Arial", 10, "bold"))


def visualize_undirected_graph_on_canvas(canvas, vertex_count, adj_matrix,
                                         circle_radius, vertex_size, window_center_x, window_center_y, loop_radius_viz,
                                         graph_color="green", fill_color="lightgreen", outline_color="darkgreen",
                                         title_text="Ненапрямлений граф"):
    canvas.create_text(window_center_x, 20, text=title_text, font=("Arial", 14, "bold"))
    vertex_positions = calculate_vertex_positions(circle_radius, vertex_count, window_center_x, window_center_y)

    for i in range(vertex_count):
        for j in range(i, vertex_count):
            if adj_matrix[i][j] == 1:
                x1_node, y1_node = vertex_positions[i]
                x2_node, y2_node = vertex_positions[j]

                if i == j:
                    angle = -math.pi / 2 + 2 * math.pi * i / vertex_count
                    draw_self_loop(canvas, x1_node, y1_node, angle, loop_radius=loop_radius_viz,
                                   vertex_size=vertex_size, color=graph_color, is_directed=False)
                else:
                    delta_x = x2_node - x1_node;
                    delta_y = y2_node - y1_node
                    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
                    if distance == 0: continue

                    start_x = x1_node + vertex_size * delta_x / distance
                    start_y = y1_node + vertex_size * delta_y / distance
                    end_x = x2_node - vertex_size * delta_x / distance
                    end_y = y2_node - vertex_size * delta_y / distance

                    canvas.create_line(start_x, start_y, end_x, end_y, fill=graph_color, width=1.5)

    for i, (x, y) in enumerate(vertex_positions):
        canvas.create_oval(x - vertex_size, y - vertex_size, x + vertex_size, y + vertex_size, fill=fill_color,
                           outline=outline_color)
        canvas.create_text(x, y, text=str(i + 1), fill="black", font=("Arial", 10, "bold"))


def visualize_condensation_graph_on_canvas(canvas, vertex_count, adj_matrix, labels_scc,
                                           circle_radius, vertex_size_orig, window_center_x, window_center_y,
                                           loop_radius_viz,
                                           graph_color="black", fill_color="white", outline_color="green",
                                           title_text="Граф конденсації"):
    canvas.create_text(window_center_x, 20, text=title_text, font=("Arial", 14, "bold"))

    current_circle_radius = circle_radius
    if vertex_count == 2:
        current_circle_radius = circle_radius * 0.3
    elif vertex_count < 5 and vertex_count > 1:
        current_circle_radius = circle_radius * 0.7
    elif vertex_count == 1:
        current_circle_radius = circle_radius * 0.3
    elif vertex_count == 0:
        return

    vertex_positions = calculate_vertex_positions(current_circle_radius, vertex_count, window_center_x, window_center_y)

    if vertex_count == 2:
        spacing_x = window_center_x * 0.5
        y_pos = window_center_y
        vertex_positions = [
            (window_center_x - spacing_x, y_pos),
            (window_center_x + spacing_x, y_pos)
        ]

    v_size = vertex_size_orig * 1.8
    font_size = 12

    for i in range(vertex_count):
        for j in range(vertex_count):
            if adj_matrix[i][j] == 1:
                x1_node, y1_node = vertex_positions[i]
                x2_node, y2_node = vertex_positions[j]

                delta_x = x2_node - x1_node;
                delta_y = y2_node - y1_node
                distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
                if distance == 0: continue

                start_x = x1_node + v_size * delta_x / distance
                start_y = y1_node + v_size * delta_y / distance
                end_x = x2_node - v_size * delta_x / distance
                end_y = y2_node - v_size * delta_y / distance

                draw_arrow(canvas, start_x, start_y, end_x, end_y, color=graph_color, arrow_size=12, line_dash=(4, 4))

    for i, (x, y) in enumerate(vertex_positions):
        canvas.create_oval(x - v_size, y - v_size, x + v_size, y + v_size,
                           fill=fill_color, outline=outline_color, width=2.5)
        node_label = str(i + 1)
        canvas.create_text(x, y, text=node_label, fill="black", font=("Arial", font_size, "bold"))