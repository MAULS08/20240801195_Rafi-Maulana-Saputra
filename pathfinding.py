import heapq
import math
import time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Ukuran peta dan koordinat awal/tujuan.
ROWS, COLS = 15, 15
START, GOAL = (1, 1), (13, 13)
NORMAL, OBSTACLE, MUD, SAND = 0, 1, 2, 3
TERRAIN_COST = {NORMAL: 1, MUD: 4, SAND: 7}

# Function ini digunakan untuk membuat peta 15x15 berisi rintangan dan medan berbobot.
def create_map():
    """Membuat peta grid 15x15 dengan rintangan, lumpur, dan pasir."""
    grid = [[NORMAL for _ in range(COLS)] for _ in range(ROWS)]
    obstacles = (
        [(r, 4) for r in range(1, 12) if r not in (3, 7, 10)]
        + [(r, 8) for r in range(3, 15) if r not in (5, 9, 12)]
        + [(10, c) for c in range(1, 7) if c not in (2, 5)]
        + [(5, c) for c in range(9, 14) if c not in (10, 12)]
        + [(r, 11) for r in range(7, 13) if r not in (8, 11)]
    )
    for r, c in obstacles:
        grid[r][c] = OBSTACLE
    for r in range(2, 6):
        for c in range(6, 8):
            if grid[r][c] != OBSTACLE:
                grid[r][c] = MUD
    for r in range(10, 14):
        for c in range(9, 14):
            if grid[r][c] != OBSTACLE:
                grid[r][c] = SAND
    grid[START[0]][START[1]] = NORMAL
    grid[GOAL[0]][GOAL[1]] = NORMAL
    return grid

# Function ini mencari tetangga atas, bawah, kiri, dan kanan yang valid.
def get_neighbors(grid, node):
    """Mengembalikan tetangga valid yang tidak berada di luar peta/rintangan."""
    r, c = node
    candidates = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    return [(nr, nc) for nr, nc in candidates
            if 0 <= nr < ROWS and 0 <= nc < COLS
            and grid[nr][nc] != OBSTACLE]

# Function ini memperkirakan jarak node ke goal menggunakan Manhattan Distance.
def heuristic(node, goal):
    """Menghitung estimasi jarak untuk gerakan empat arah."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Function ini menyusun kembali jalur dari start sampai goal menggunakan parent.
def reconstruct_path(parent, start, goal):
    """Merekonstruksi jalur berdasarkan hubungan parent setiap node."""
    if goal not in parent:
        return []
    path, current = [], goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path if path and path[0] == start else []

# Function ini mencari jalur berbiaya minimum dengan algoritma Dijkstra.
def dijkstra(grid, start, goal):
    """Dijkstra memprioritaskan biaya aktual dari start."""
    began = time.perf_counter()
    frontier = [(0, start)]
    distance, parent, explored = {start: 0}, {start: None}, set()
    while frontier:
        current_cost, current = heapq.heappop(frontier)
        if current in explored or current_cost != distance.get(current):
            continue
        explored.add(current)
        if current == goal:
            break
        for neighbor in get_neighbors(grid, current):
            step_cost = TERRAIN_COST[grid[neighbor[0]][neighbor[1]]]
            new_cost = current_cost + step_cost
            if new_cost < distance.get(neighbor, math.inf):
                distance[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))
    path = reconstruct_path(parent, start, goal)
    return {"path": path, "cost": distance.get(goal, math.inf),
            "steps": max(0, len(path)-1), "explored": len(explored),
            "explored_nodes": explored, "time_ms": (time.perf_counter()-began)*1000}

# Function ini mencari jalur menggunakan biaya aktual ditambah estimasi ke goal.
def astar(grid, start, goal):
    """A* memprioritaskan f(n) = g(n) + h(n)."""
    began = time.perf_counter()
    frontier = [(heuristic(start, goal), 0, start)]
    distance, parent, explored = {start: 0}, {start: None}, set()
    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        if current in explored or current_cost != distance.get(current):
            continue
        explored.add(current)
        if current == goal:
            break
        for neighbor in get_neighbors(grid, current):
            step_cost = TERRAIN_COST[grid[neighbor[0]][neighbor[1]]]
            new_cost = current_cost + step_cost
            if new_cost < distance.get(neighbor, math.inf):
                distance[neighbor] = new_cost
                parent[neighbor] = current
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, new_cost, neighbor))
    path = reconstruct_path(parent, start, goal)
    return {"path": path, "cost": distance.get(goal, math.inf),
            "steps": max(0, len(path)-1), "explored": len(explored),
            "explored_nodes": explored, "time_ms": (time.perf_counter()-began)*1000}

# Function ini menampilkan perbandingan metrik hasil Dijkstra dan A*.
def print_comparison(dres, ares):
    """Mencetak biaya jalur, langkah, node eksplorasi, dan waktu."""
    print("\\n=== PERBANDINGAN HASIL PETA 15x15 ===")
    print(f"{'Metrik':<24}{'Dijkstra':>12}{'A*':>12}")
    print("-" * 48)
    for label, key in [("Biaya jalur", "cost"), ("Jumlah langkah", "steps"),
                       ("Node dieksplorasi", "explored"), ("Waktu (ms)", "time_ms")]:
        print(f"{label:<24}{dres[key]:>12.3f}{ares[key]:>12.3f}" if key == "time_ms"
              else f"{label:<24}{str(dres[key]):>12}{str(ares[key]):>12}")

# Function ini menggambar peta, node eksplorasi, start, goal, dan jalur yang ditemukan.
def draw_results(grid, dres, ares, output_path="hasil_pathfinding_15x15.png"):
    """Membuat visualisasi hasil algoritma dalam dua panel."""
    cmap = ListedColormap(["#f4f4f4", "#333333", "#d9a441", "#d9c7a0"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    for ax, name, result, color in [
        (axes[0], "Dijkstra", dres, "#1565c0"),
        (axes[1], "A*", ares, "#d32f2f")
    ]:
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, origin="upper")
        nodes = result["explored_nodes"]
        if nodes:
            ax.scatter([n[1] for n in nodes], [n[0] for n in nodes],
                       s=15, c="#80cbc4", alpha=.55, label="Node dieksplorasi")
        path = result["path"]
        if path:
            ax.plot([n[1] for n in path], [n[0] for n in path],
                    color=color, linewidth=2.5, marker="o", markersize=3, label="Jalur")
        ax.scatter(START[1], START[0], marker="s", s=100, c="#2e7d32", label="Start")
        ax.scatter(GOAL[1], GOAL[0], marker="*", s=170, c="#ffb300",
                   edgecolors="black", label="Goal")
        ax.set_title(f"{name}\\nBiaya: {result['cost']} | Node: {result['explored']}")
        ax.set_xticks(range(COLS)); ax.set_yticks(range(ROWS))
        ax.set_xticks([x-.5 for x in range(1, COLS)], minor=True)
        ax.set_yticks([y-.5 for y in range(1, ROWS)], minor=True)
        ax.grid(which="minor", color="#bdbdbd", linewidth=.35)
        ax.tick_params(length=0)
        ax.legend(loc="upper left", fontsize=7)
    fig.legend(handles=[
        Patch(facecolor="#f4f4f4", edgecolor="#999", label="Normal (biaya 1)"),
        Patch(facecolor="#333333", label="Rintangan"),
        Patch(facecolor="#d9a441", label="Lumpur (biaya 4)"),
        Patch(facecolor="#d9c7a0", label="Pasir (biaya 7)")],
        loc="lower center", ncol=4)
    fig.suptitle("Pathfinding 15x15: Dijkstra vs A*", fontsize=14, fontweight="bold")
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"\\nVisualisasi disimpan sebagai {output_path}")

# Function ini menjalankan program dari pembuatan peta hingga visualisasi hasil.
def main():
    """Menjalankan seluruh eksperimen pathfinding."""
    grid = create_map()
    dres = dijkstra(grid, START, GOAL)
    ares = astar(grid, START, GOAL)
    print_comparison(dres, ares)
    draw_results(grid, dres, ares)

if __name__ == "__main__":
    main()
