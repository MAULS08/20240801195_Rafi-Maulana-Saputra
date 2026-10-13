import heapq, math, time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ROWS, COLS = 20, 20
START, GOAL = (1, 1), (18, 18)
NORMAL, OBSTACLE, MUD, SAND = 0, 1, 2, 3
TERRAIN_COST = {NORMAL: 1, MUD: 4, SAND: 7}

# Function ini digunakan untuk membuat peta berbentuk grid 20x20,
# lalu menempatkan rintangan serta area lumpur dan pasir yang memiliki biaya berbeda.
def create_map():
    """Membuat grid 20x20 berisi rintangan dan medan dengan biaya berbeda."""
    grid = [[NORMAL for _ in range(COLS)] for _ in range(ROWS)]
    obstacles = (
        [(r, 5) for r in range(1, 16) if r not in (4, 10, 13)]
        + [(r, 10) for r in range(4, 20) if r not in (7, 12, 16)]
        + [(12, c) for c in range(2, 9) if c not in (4, 7)]
        + [(6, c) for c in range(11, 18) if c not in (14, 16)]
        + [(r, 15) for r in range(8, 18) if r not in (11, 14)]
    )
    for r, c in obstacles:
        grid[r][c] = OBSTACLE
    for r in range(2, 8):
        for c in range(7, 10):
            if grid[r][c] != OBSTACLE:
                grid[r][c] = MUD
    for r in range(14, 19):
        for c in range(12, 18):
            if grid[r][c] != OBSTACLE:
                grid[r][c] = SAND
    grid[START[0]][START[1]] = NORMAL
    grid[GOAL[0]][GOAL[1]] = NORMAL
    return grid

# Function ini digunakan untuk mencari kotak tetangga yang bisa dilewati
# dari posisi saat ini, yaitu atas, bawah, kiri, dan kanan.
def get_neighbors(grid, node):
    """Mengembalikan tetangga valid ke atas, bawah, kiri, dan kanan."""
    r, c = node
    candidates = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    return [(nr,nc) for nr,nc in candidates
            if 0 <= nr < ROWS and 0 <= nc < COLS
            and grid[nr][nc] != OBSTACLE]

# Function ini digunakan untuk menghitung estimasi jarak dari posisi saat ini
# menuju tujuan menggunakan Manhattan Distance, tanpa menghitung rintangan.
def heuristic(node, goal):
    """Menghitung jarak Manhattan; sesuai untuk gerakan empat arah."""
    return abs(node[0]-goal[0]) + abs(node[1]-goal[1])

# Function ini digunakan untuk menyusun jalur akhir dari titik start ke goal
# berdasarkan catatan parent yang dibuat selama pencarian.
def reconstruct_path(parent, start, goal):
    """Menyusun jalur dari goal ke start melalui parent, lalu membalik urutannya."""
    if goal not in parent:
        return []
    path, current = [], goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent.get(current)
    if not path or path[-1] != start:
        return []
    return path[::-1]

# Function ini digunakan untuk mencari jalur dengan total biaya paling rendah
# menggunakan algoritma Dijkstra, dengan mempertimbangkan biaya setiap jenis medan.
def dijkstra(grid, start, goal):
    """Mencari jalur biaya minimum dengan prioritas g(n), biaya aktual."""
    frontier = [(0, start)]
    distance, parent, explored = {start: 0}, {start: None}, set()
    while frontier:
        current_cost, current = heapq.heappop(frontier)
        if current_cost != distance.get(current, math.inf) or current in explored:
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
    return {"path": reconstruct_path(parent,start,goal),
            "cost": distance.get(goal, math.inf),
            "explored": len(explored), "explored_nodes": explored}

# Function ini digunakan untuk mencari jalur dengan algoritma A*; prioritasnya
# adalah biaya yang sudah ditempuh ditambah estimasi biaya menuju tujuan.
def astar(grid, start, goal):
    """Mencari jalur dengan f(n)=g(n)+h(n), biaya aktual plus estimasi."""
    frontier = [(heuristic(start,goal), 0, start)]
    distance, parent, explored = {start: 0}, {start: None}, set()
    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        if current_cost != distance.get(current, math.inf) or current in explored:
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
                heapq.heappush(frontier, (priority,new_cost,neighbor))
    return {"path": reconstruct_path(parent,start,goal),
            "cost": distance.get(goal, math.inf),
            "explored": len(explored), "explored_nodes": explored}

# Function ini digunakan untuk menampilkan perbandingan hasil Dijkstra dan A*
# seperti biaya jalur, jumlah langkah, jumlah node yang dieksplorasi, dan waktu.
def print_comparison(dres, ares):
    """Mencetak biaya, jumlah langkah, node eksplorasi, dan waktu eksekusi."""
    print("\\n=== PERBANDINGAN HASIL ===")
    print(f"{'Metrik':<25}{'Dijkstra':>12}{'A*':>12}")
    print("-"*49)
    for label,key in [("Biaya jalur","cost"),("Jumlah langkah","steps"),
                      ("Node dieksplorasi","explored"),("Waktu (ms)","time_ms")]:
        d,a = dres[key],ares[key]
        if key == "time_ms":
            print(f"{label:<25}{d:>12.3f}{a:>12.3f}")
        else:
            print(f"{label:<25}{str(d):>12}{str(a):>12}")

# Function ini digunakan untuk menggambar peta dan menampilkan jalur hasil
# Dijkstra serta A*, termasuk rintangan, medan, start, goal, dan node eksplorasi.
def draw_results(grid, dres, ares):
    """Memvisualisasikan medan, rintangan, node eksplorasi, dan jalur solusi."""
    cmap = ListedColormap(["#f4f4f4","#333333","#d9a441","#d9c7a0"])
    fig, axes = plt.subplots(1,2,figsize=(14,7),constrained_layout=True)
    for ax,name,res,color in [(axes[0],"Dijkstra",dres,"#1565c0"),
                              (axes[1],"A*",ares,"#d32f2f")]:
        ax.imshow(grid,cmap=cmap,vmin=0,vmax=3,origin="upper")
        nodes = res["explored_nodes"]
        if nodes:
            ax.scatter([n[1] for n in nodes],[n[0] for n in nodes],
                       s=12,c="#80cbc4",alpha=.55,label="Node dieksplorasi")
        path = res["path"]
        if path:
            ax.plot([n[1] for n in path],[n[0] for n in path],
                    color=color,linewidth=2.8,marker="o",markersize=3,label="Jalur")
        ax.scatter(START[1],START[0],marker="s",s=120,c="#2e7d32",label="Start")
        ax.scatter(GOAL[1],GOAL[0],marker="*",s=190,c="#ffb300",
                   edgecolors="black",label="Goal")
        ax.set_title(f"{name}\\nBiaya: {res['cost']} | Node: {res['explored']}")
        ax.set_xticks(range(COLS)); ax.set_yticks(range(ROWS))
        ax.set_xticklabels(range(COLS),fontsize=7); ax.set_yticklabels(range(ROWS),fontsize=7)
        ax.set_xticks([x-.5 for x in range(1,COLS)],minor=True)
        ax.set_yticks([y-.5 for y in range(1,ROWS)],minor=True)
        ax.grid(which="minor",color="#bdbdbd",linewidth=.35)
        ax.tick_params(length=0); ax.set_xlim(-.5,COLS-.5); ax.set_ylim(ROWS-.5,-.5)
        ax.legend(loc="upper left",fontsize=7)
    fig.legend(handles=[
        Patch(facecolor="#f4f4f4",edgecolor="#999999",label="Normal (biaya 1)"),
        Patch(facecolor="#333333",label="Rintangan"),
        Patch(facecolor="#d9a441",label="Lumpur (biaya 4)"),
        Patch(facecolor="#d9c7a0",label="Pasir (biaya 7)")],
        loc="lower center",ncol=4)
    fig.suptitle("Pathfinding Game 2D: Dijkstra vs A*",fontsize=15,fontweight="bold")
    plt.savefig("hasil_pathfinding.png",dpi=180,bbox_inches="tight")
    print("\\nVisualisasi disimpan sebagai hasil_pathfinding.png")
    plt.show()

# Function ini digunakan sebagai fungsi utama untuk membuat peta, menjalankan
# kedua algoritma, menghitung metrik, membandingkan hasil, dan menampilkan visualisasi.
def main():
    """Menjalankan dua algoritma, membandingkan metrik, lalu menampilkan visualisasi."""
    grid = create_map()
    t = time.perf_counter(); dres = dijkstra(grid,START,GOAL)
    dres["time_ms"] = (time.perf_counter()-t)*1000
    t = time.perf_counter(); ares = astar(grid,START,GOAL)
    ares["time_ms"] = (time.perf_counter()-t)*1000
    dres["steps"] = max(0,len(dres["path"])-1)
    ares["steps"] = max(0,len(ares["path"])-1)
    print(f"Ukuran peta: {ROWS} x {COLS}; Start: {START}; Goal: {GOAL}")
    print_comparison(dres,ares)
    print("\\nValidasi biaya optimal:", "SAMA" if dres["cost"] == ares["cost"] else "BERBEDA")
    draw_results(grid,dres,ares)

if __name__ == "__main__":
    main()
