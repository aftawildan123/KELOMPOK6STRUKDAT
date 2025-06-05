import heapq
from itertools import permutations

# ================================
# Fungsi bantu
# ================================
def waktu_tempuh(jarak_km, kecepatan_motor=50):
    waktu_jam = jarak_km / kecepatan_motor
    jam = int(waktu_jam)
    menit = int((waktu_jam - jam) * 60)
    return f"{jam} jam {menit} menit"

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name):
        self.vertices[name] = {}

    def add_edge(self, from_city, to_city, weight):
        self.vertices[from_city][to_city] = weight
        self.vertices[to_city][from_city] = weight

# Kota
kota_jatim = [
    "Surabaya", "Malang", "Kediri", "Blitar", "Tulungagung",
    "Madiun", "Lamongan", "Gresik", "Bojonegoro", "Jombang"
]

# Buat graph
graph = Graph()
for kota in kota_jatim:
    graph.add_vertex(kota)

edges = [
    ("Surabaya", "Malang", 90),
    ("Surabaya", "Kediri", 122),
    ("Surabaya", "Blitar", 155),
    ("Surabaya", "Tulungagung", 170),
    ("Surabaya", "Madiun", 173),
    ("Surabaya", "Lamongan", 52),
    ("Surabaya", "Gresik", 25),
    ("Surabaya", "Bojonegoro", 120),
    ("Surabaya", "Jombang", 82),
    ("Malang", "Kediri", 86),
    ("Malang", "Blitar", 72),
    ("Malang", "Tulungagung", 88),
    ("Malang", "Madiun", 130),
    ("Malang", "Jombang", 95),
    ("Kediri", "Blitar", 40),
    ("Kediri", "Tulungagung", 35),
    ("Kediri", "Madiun", 100),
    ("Kediri", "Jombang", 40),
    ("Kediri", "Bojonegoro", 75),
    ("Kediri", "Lamongan", 115),
    ("Blitar", "Tulungagung", 30),
    ("Blitar", "Madiun", 85),
    ("Tulungagung", "Madiun", 75),
    ("Madiun", "Jombang", 110),
    ("Lamongan", "Gresik", 30),
    ("Lamongan", "Jombang", 95),
    ("Lamongan", "Bojonegoro", 70),
    ("Gresik", "Jombang", 85),
    ("Gresik", "Bojonegoro", 100),
    ("Bojonegoro", "Jombang", 90)
]

for u, v, w in edges:
    graph.add_edge(u, v, w)

# Dijkstra
def dijkstra(graph, start, end):
    distances = {v: float('infinity') for v in graph.vertices}
    distances[start] = 0
    prev = {}
    queue = [(0, start)]

    while queue:
        curr_dist, curr = heapq.heappop(queue)
        if curr == end:
            break
        for neighbor, weight in graph.vertices[curr].items():
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                prev[neighbor] = curr
                heapq.heappush(queue, (distance, neighbor))

    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev.get(node)
        if node is None:
            return [], float('inf')
    path.append(start)
    path.reverse()
    return path, distances[end]

# TSP brute-force
def tsp_brute_force(graph, start):
    cities = list(graph.vertices.keys())
    cities.remove(start)
    min_path = []
    min_dist = float('inf')

    for perm in permutations(cities):
        path = [start] + list(perm) + [start]
        total = 0
        valid = True
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            if v in graph.vertices[u]:
                total += graph.vertices[u][v]
            else:
                valid = False
                break
        if valid and total < min_dist:
            min_path = path
            min_dist = total

    return min_path, min_dist

# Main program (dengan perulangan)
def main():
    print("=== PROGRAM GRAF JAWA TIMUR (DIJKSTRA + TSP) ===")
    while True:
        print("\nDaftar Kota:")
        for kota in kota_jatim:
            print("-", kota)

        asal = input("\nMasukkan kota asal (atau 'exit' untuk keluar): ").title()
        if asal.lower() == 'exit':
            break

        tujuan = input("Masukkan kota tujuan: ").title()
        if tujuan.lower() == 'exit':
            break

        if asal not in kota_jatim or tujuan not in kota_jatim:
            print("Kota tidak valid.")
            continue

        path, dist = dijkstra(graph, asal, tujuan)
        if path:
            print(f"\n Jalur tercepat dari {asal} ke {tujuan}: {' -> '.join(path)}")
            print(f"Total jarak: {dist} km")
            print(f"Estimasi waktu tempuh: {waktu_tempuh(dist)}")
        else:
            print("Tidak ada jalur yang ditemukan.")

        tsp_path, tsp_total = tsp_brute_force(graph, asal)
        print("\n Rute TSP terbaik:")
        print(" -> ".join(tsp_path))
        print(f"Total jarak: {tsp_total} km")
        print(f"Estimasi waktu tempuh (motor): {waktu_tempuh(tsp_total)}")

if __name__ == "__main__":
    main()
