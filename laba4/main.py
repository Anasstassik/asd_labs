import tkinter as tk
from datetime import datetime

import graph_generator as gen
import graph_analyzer as analyze
import graph_visualizer as viz

SEED = 4310
N = 11
N3_VAL = 1
N4_VAL = 0

K_PART1 = 1.0 - N3_VAL * 0.01 - N4_VAL * 0.01 - 0.3
K_PART2 = 1.0 - N3_VAL * 0.005 - N4_VAL * 0.005 - 0.27

VIZ_CIRCLE_RADIUS = 225
VIZ_VERTEX_SIZE = 16
VIZ_WINDOW_WIDTH = 610
VIZ_WINDOW_HEIGHT = 630
VIZ_WINDOW_CENTER_X = VIZ_WINDOW_WIDTH // 2
VIZ_WINDOW_CENTER_Y = VIZ_WINDOW_HEIGHT // 2 + 20
VIZ_LOOP_RADIUS = 45


def main():
    print(f"Коефіцієнт k1={K_PART1:.4f}")
    adj_matrix_dir1 = gen.create_directed_graph_matrix(N, K_PART1, SEED)
    adj_matrix_undir1 = gen.convert_to_undirected_graph(adj_matrix_dir1)

    gen.display_matrix(adj_matrix_dir1, f"Adir1 (k1={K_PART1:.3f}, N={N})")
    gen.display_matrix(adj_matrix_undir1, f"Aundir1 (з Adir1, k1={K_PART1:.3f}, N={N})")

    print(f"\n--- Характеристики для графів з k1={K_PART1:.3f} ---")
    undir_degrees1 = analyze.calculate_undirected_degrees(adj_matrix_undir1)
    print("\nСтепені вершин Aundir1:")
    for i, degree in enumerate(undir_degrees1): print(f"Вершина {i + 1}: {degree}")

    dir_out_deg1, dir_in_deg1 = analyze.calculate_directed_degrees(adj_matrix_dir1)
    print(f"\nНапівстепені вершин Adir1 (k1={K_PART1:.3f}):")
    print("Вершина | Вихід | Захід");
    print("-----------------------")
    for i in range(N): print(f"{i + 1:^7} | {dir_out_deg1[i]:^5} | {dir_in_deg1[i]:^5}")

    dir_total_deg1 = [o + i for o, i in zip(dir_out_deg1, dir_in_deg1)]
    print(f"\nПовні степені вершин Adir1 (k1={K_PART1:.3f}, вихід + захід):")
    for i, degree in enumerate(dir_total_deg1): print(f"Вершина {i + 1}: {degree}")

    is_undir_reg1, undir_reg_deg1 = analyze.check_undirected_regularity(undir_degrees1)
    print(f"\nAundir1 однорідний: {'Так' if is_undir_reg1 else 'Ні'}")
    if is_undir_reg1: print(f"Степінь однорідності: {undir_reg_deg1}")

    is_dir_reg1, dir_reg_deg1 = analyze.check_directed_regularity(dir_out_deg1, dir_in_deg1)
    print(f"\nAdir1 (k1={K_PART1:.3f}) однорідний: {'Так' if is_dir_reg1 else 'Ні'}")
    if is_dir_reg1: print(f"Степінь однорідності: {dir_reg_deg1}")

    undir_pend1, undir_isol1 = analyze.find_special_vertices_undirected(undir_degrees1)
    print("\nДля Aundir1:")
    print(f"Висячі вершини: {undir_pend1 if undir_pend1 else 'немає'}")
    print(f"Ізольовані вершини: {undir_isol1 if undir_isol1 else 'немає'}")

    dir_pend1, dir_isol1 = analyze.find_special_vertices_directed(dir_out_deg1, dir_in_deg1)
    print(f"\nДля Adir1 (k1={K_PART1:.3f}):")
    print(f"Висячі вершини: {dir_pend1 if dir_pend1 else 'немає'}")
    print(f"Ізольовані вершини: {dir_isol1 if dir_isol1 else 'немає'}")

    root_main_window = tk.Tk()
    root_main_window.title(f"ЛР4 - Журавель Анастасія, ІМ-43 - Варіант {SEED}")
    current_date = datetime.now().strftime("%d.%m.%Y")

    buttons_frame_k1 = tk.LabelFrame(root_main_window, text=f"Графи для k1={K_PART1:.3f}", padx=5, pady=5)
    buttons_frame_k1.pack(padx=10, pady=5, fill="x")

    def show_dir1_window():
        win = tk.Toplevel(root_main_window)
        tk.Label(win, text="Лабораторна 4 Журавель Анастасія").pack(pady=2)
        canvas = tk.Canvas(win, width=VIZ_WINDOW_WIDTH, height=VIZ_WINDOW_HEIGHT, bg="white", borderwidth=1,
                           relief="solid")
        canvas.pack(padx=10, pady=5)
        viz.visualize_directed_graph_on_canvas(canvas, N, adj_matrix_dir1,
                                               VIZ_CIRCLE_RADIUS, VIZ_VERTEX_SIZE, VIZ_WINDOW_CENTER_X,
                                               VIZ_WINDOW_CENTER_Y, VIZ_LOOP_RADIUS,
                                               graph_color="blue", fill_color="lightblue", outline_color="navy",
                                               title_text=f"Напрямлений граф (k1={K_PART1:.3f})")

    def show_undir1_window():
        win = tk.Toplevel(root_main_window)
        tk.Label(win, text="Лабораторна 4 Журавель Анастасія").pack(pady=2)
        canvas = tk.Canvas(win, width=VIZ_WINDOW_WIDTH, height=VIZ_WINDOW_HEIGHT, bg="white", borderwidth=1,
                           relief="solid")
        canvas.pack(padx=10, pady=5)
        viz.visualize_undirected_graph_on_canvas(canvas, N, adj_matrix_undir1,
                                                 VIZ_CIRCLE_RADIUS, VIZ_VERTEX_SIZE, VIZ_WINDOW_CENTER_X,
                                                 VIZ_WINDOW_CENTER_Y, VIZ_LOOP_RADIUS,
                                                 graph_color="green", fill_color="lightgreen",
                                                 outline_color="darkgreen",
                                                 title_text=f"Ненапрямлений граф (k1={K_PART1:.3f})")

    tk.Button(buttons_frame_k1, text="Показати Adir1", command=show_dir1_window).pack(side=tk.LEFT, padx=5)
    tk.Button(buttons_frame_k1, text="Показати Aundir1", command=show_undir1_window).pack(side=tk.LEFT, padx=5)


    adj_matrix_dir2 = gen.create_directed_graph_matrix(N, K_PART2, SEED)
    gen.display_matrix(adj_matrix_dir2, f"Adir2 (k2={K_PART2:.3f}, N={N})")

    print(f"\n--- Характеристики для Adir2 (k2={K_PART2:.3f}) ---")
    dir_out_deg2, dir_in_deg2 = analyze.calculate_directed_degrees(adj_matrix_dir2)
    print(f"\nНапівстепені вершин Adir2:")
    print("Вершина | Вихід | Захід");
    print("-----------------------")
    for i in range(N): print(f"{i + 1:^7} | {dir_out_deg2[i]:^5} | {dir_in_deg2[i]:^5}")

    paths_len2 = analyze.find_paths_of_length(adj_matrix_dir2, 2)
    print(f"\nШляхи довжини 2 в Adir2 (знайдено {len(paths_len2)}):")
    if paths_len2:
        for p in paths_len2:
            print(p)
    else:
        print("Немає шляхів довжини 2.")

    paths_len3 = analyze.find_paths_of_length(adj_matrix_dir2, 3)
    print(f"\nШляхи довжини 3 в Adir2 (знайдено {len(paths_len3)}):")
    if paths_len3:
        for p in paths_len3:
            print(p)
    else:
        print("Немає шляхів довжини 3.")

    reach_matrix2 = analyze.warshall_reachability_matrix(adj_matrix_dir2)
    gen.display_matrix(reach_matrix2, "Матриця досяжності R для Adir2")

    s_conn_matrix2 = analyze.strong_connectivity_matrix(reach_matrix2)
    gen.display_matrix(s_conn_matrix2, "Матриця сильної зв'язності S для Adir2")

    scc_list2 = analyze.find_strongly_connected_components(s_conn_matrix2)
    print("\nКомпоненти сильної зв'язності для Adir2:")
    if scc_list2:
        for i, component in enumerate(scc_list2): print(f"Компонента {i + 1}: {component}")
    else:
        print("Компонент сильної зв'язності не знайдено.")

    buttons_frame_k2 = tk.LabelFrame(root_main_window, text=f"Графи для k2={K_PART2:.3f}", padx=5, pady=5)
    buttons_frame_k2.pack(padx=10, pady=10, fill="x")

    def show_dir2_window():
        win = tk.Toplevel(root_main_window)
        tk.Label(win, text="Лабораторна 4 Журавель Анастасія").pack(pady=2)
        canvas = tk.Canvas(win, width=VIZ_WINDOW_WIDTH, height=VIZ_WINDOW_HEIGHT, bg="white", borderwidth=1,
                           relief="solid")
        canvas.pack(padx=10, pady=5)
        viz.visualize_directed_graph_on_canvas(canvas, N, adj_matrix_dir2,
                                               VIZ_CIRCLE_RADIUS, VIZ_VERTEX_SIZE, VIZ_WINDOW_CENTER_X,
                                               VIZ_WINDOW_CENTER_Y, VIZ_LOOP_RADIUS,
                                               graph_color="maroon", fill_color="lightcoral", outline_color="darkred",
                                               title_text=f"Напрямлений граф (k2={K_PART2:.3f})")

    tk.Button(buttons_frame_k2, text="Показати Adir2", command=show_dir2_window).pack(side=tk.LEFT, padx=5)

    if scc_list2:
        condensation_adj2, condensation_labels2 = analyze.build_condensation_graph(adj_matrix_dir2, scc_list2)
        gen.display_matrix(condensation_adj2, "Матриця суміжності графа конденсації для Adir2")
        print("\nМітки вершин графа конденсації Adir2 (оригінальні компоненти):", condensation_labels2)

        if condensation_adj2 or (not condensation_adj2 and len(scc_list2) == 1):
            def show_condensation2_window():
                win = tk.Toplevel(root_main_window)
                tk.Label(win, text="Лабораторна 4 Журавель Анастасія").pack(pady=2)
                canvas = tk.Canvas(win, width=VIZ_WINDOW_WIDTH, height=VIZ_WINDOW_HEIGHT, bg="white", borderwidth=1,
                                   relief="solid")
                canvas.pack(padx=10, pady=5)
                num_components_to_draw = len(condensation_adj2) if condensation_adj2 and condensation_adj2[0] else len(
                    scc_list2)

                viz.visualize_condensation_graph_on_canvas(canvas, num_components_to_draw, condensation_adj2,
                                                           labels_scc=condensation_labels2,
                                                           circle_radius=VIZ_CIRCLE_RADIUS,
                                                           vertex_size_orig=VIZ_VERTEX_SIZE,
                                                           window_center_x=VIZ_WINDOW_CENTER_X,
                                                           window_center_y=VIZ_WINDOW_CENTER_Y,
                                                           loop_radius_viz=VIZ_LOOP_RADIUS,
                                                           graph_color="black",
                                                           fill_color="white",
                                                           outline_color="green",
                                                           title_text="Condensation of modified graph:")

            tk.Button(buttons_frame_k2, text="Показати граф конденсації Adir2", command=show_condensation2_window).pack(
                side=tk.LEFT, padx=5)
        else:
            print("Граф конденсації для Adir2 порожній (немає ребер між компонентами і більше 1 компоненти).")
    else:
        print("Неможливо побудувати граф конденсації для Adir2.")

    root_main_window.mainloop()


if __name__ == "__main__":
    main()