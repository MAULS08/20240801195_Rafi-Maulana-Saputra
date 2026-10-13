# TUGAS TOWER OF HANOI MENGGUNAKAN PYTHON

## 1. Deskripsi Program
Program Tower of Hanoi merupakan program untuk menyelesaikan permainan pemindahan cakram dari tiang awal ke tiang tujuan dengan bantuan satu tiang perantara.

Program ini dibuat menggunakan bahasa pemrograman Python dengan menerapkan algoritma rekursi (*recursion*).

## 2. Tujuan Program
Tujuan program ini adalah memindahkan seluruh cakram dari tiang A sebagai titik awal (*Start*) ke tiang C sebagai titik tujuan (*Finish*), sedangkan tiang B digunakan sebagai tiang bantuan.

## 3. Aturan Permainan
1. Hanya satu cakram yang boleh dipindahkan dalam satu langkah.
2. Hanya cakram paling atas yang boleh dipindahkan.
3. Cakram berukuran besar tidak boleh diletakkan di atas cakram yang lebih kecil.

## 4. Penjelasan Kode Program

### A. Function tower_of_hanoi()
Function `tower_of_hanoi(n, asal, bantuan, tujuan)` digunakan untuk mengatur proses pemindahan cakram.

Parameter yang digunakan:
- `n`: jumlah cakram yang akan dipindahkan.
- `asal`: tiang tempat cakram berada.
- `bantuan`: tiang perantara untuk membantu pemindahan.
- `tujuan`: tiang tujuan pemindahan cakram.

### B. Kondisi Dasar (Base Case)
Kondisi `if n == 1` digunakan untuk memeriksa apakah hanya tersisa satu cakram.

Jika kondisi terpenuhi, program menampilkan perintah pemindahan cakram dari tiang asal ke tiang tujuan, kemudian menghentikan pemanggilan fungsi tersebut menggunakan `return`.

### C. Pemanggilan Rekursif Pertama
Perintah `tower_of_hanoi(n - 1, asal, tujuan, bantuan)` digunakan untuk memindahkan sebanyak `n - 1` cakram dari tiang asal ke tiang bantuan dengan memanfaatkan tiang tujuan sebagai perantara.

### D. Pemindahan Cakram Terbesar
Perintah `print()` menampilkan langkah pemindahan cakram terbesar yang tersisa dari tiang asal ke tiang tujuan.

Pemindahan ini dilakukan setelah cakram-cakram yang lebih kecil berhasil dipindahkan.

### E. Pemanggilan Rekursif Kedua
Perintah `tower_of_hanoi(n - 1, bantuan, asal, tujuan)` digunakan untuk memindahkan cakram-cakram yang sebelumnya berada di tiang bantuan menuju tiang tujuan.

### F. Program Utama
Variabel `jumlah_cakram = 3` menentukan jumlah cakram yang digunakan.

Perintah `print()` menampilkan informasi permainan, sedangkan pemanggilan `tower_of_hanoi(jumlah_cakram, "A", "B", "C")` memulai proses pemindahan dari tiang A menuju tiang C menggunakan tiang B sebagai bantuan.

## 5. Hasil Program
Program menghasilkan tujuh langkah pemindahan sebagai berikut:

1. Pindahkan cakram 1 dari A ke C.
2. Pindahkan cakram 2 dari A ke B.
3. Pindahkan cakram 1 dari C ke B.
4. Pindahkan cakram 3 dari A ke C.
5. Pindahkan cakram 1 dari B ke A.
6. Pindahkan cakram 2 dari B ke C.
7. Pindahkan cakram 1 dari A ke C.

Setelah seluruh langkah selesai, semua cakram berada di tiang C sesuai dengan kondisi akhir pada gambar soal.

## 6. Analisis Algoritma
Algoritma yang digunakan adalah rekursi, yaitu teknik pemrograman ketika sebuah fungsi memanggil dirinya sendiri untuk menyelesaikan masalah yang lebih kecil.

Jumlah minimum langkah untuk memindahkan `n` cakram dirumuskan sebagai:

**T(n) = 2^n - 1**

Untuk tiga cakram:

T(3) = 2³ - 1 = 7 langkah.

Kompleksitas waktu algoritma adalah O(2^n), sedangkan kompleksitas ruang adalah O(n) karena kedalaman pemanggilan rekursi.

## 7. Kesimpulan
Program Tower of Hanoi berhasil menyelesaikan pemindahan tiga cakram dari tiang A ke tiang C dengan bantuan tiang B. Penerapan algoritma rekursi membuat proses pemindahan dapat dilakukan secara sistematis, dengan jumlah minimum tujuh langkah.

Program ini menunjukkan penerapan konsep rekursi, kondisi dasar, parameter fungsi, dan pemanggilan fungsi dalam bahasa Python.
