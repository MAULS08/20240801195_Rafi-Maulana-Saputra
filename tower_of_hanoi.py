
# Function utama untuk menyelesaikan permainan Tower of Hanoi.
# Parameter n = jumlah cakram yang akan dipindahkan.
# Parameter asal = tiang tempat cakram berada saat ini.
# Parameter bantuan = tiang perantara untuk membantu pemindahan.
# Parameter tujuan = tiang tempat cakram akan dipindahkan.
def tower_of_hanoi(n, asal, bantuan, tujuan):

    # Base case: jika hanya ada satu cakram,
    # pindahkan langsung dari tiang asal ke tiang tujuan.
    if n == 1:
        print(f"Pindahkan cakram 1: {asal} -> {tujuan}")
        return

    # Langkah 1:
    # Pindahkan n-1 cakram dari tiang asal ke tiang bantuan.
    # Tiang tujuan digunakan sebagai tiang perantara.
    tower_of_hanoi(n - 1, asal, tujuan, bantuan)

    # Langkah 2:
    # Setelah cakram yang lebih kecil dipindahkan,
    # pindahkan cakram terbesar yang tersisa ke tiang tujuan.
    print(f"Pindahkan cakram {n}: {asal} -> {tujuan}")

    # Langkah 3:
    # Pindahkan kembali n-1 cakram dari tiang bantuan
    # ke tiang tujuan dengan bantuan tiang asal.
    tower_of_hanoi(n - 1, bantuan, asal, tujuan)


# Menentukan jumlah cakram yang akan dipindahkan.
jumlah_cakram = 3

# Menampilkan judul program agar output lebih mudah dibaca.
print("=== TOWER OF HANOI ===")

# Menampilkan jumlah cakram yang digunakan dalam permainan.
print(f"Jumlah cakram: {jumlah_cakram}")

# Menampilkan tiang awal tempat semua cakram berada.
print("Start: A")

# Menampilkan tiang tujuan tempat semua cakram akan dipindahkan.
print("Finish: C")

# Memberikan baris kosong untuk memisahkan informasi
# permainan dengan daftar langkah pemindahan.
print()

# Memanggil function Tower of Hanoi untuk memulai proses.
# Tiga cakram dipindahkan dari tiang A ke tiang C
# dengan menggunakan tiang B sebagai bantuan.
tower_of_hanoi(jumlah_cakram, "A", "B", "C")
