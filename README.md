# Email Access Checker

Email Access Checker adalah alat otomatis yang digunakan untuk memeriksa akses ke akun email dari berbagai domain populer. Alat ini mendukung penggunaan proxy dan memungkinkan pengecekan kredensial email secara paralel untuk meningkatkan efisiensi. Selain itu, alat ini dilengkapi dengan logging untuk mencatat hasil dari setiap percobaan login.

## Fitur

- Mendukung berbagai domain email populer (Gmail, Yahoo, Outlook, dll.).
- Mendukung penggunaan proxy untuk melindungi identitas pengguna.
- Pengecekan akun email dilakukan secara paralel untuk efisiensi waktu.
- Retry mechanism pada permintaan HTTP untuk meningkatkan keandalan.
- Logging otomatis hasil login dan error ke file log (`email_checker.log`).
- Menggunakan `ThreadPoolExecutor` untuk memproses beberapa email secara bersamaan.
- Penanganan error dan timeout yang lebih baik, termasuk pemilihan proxy acak.

## Persyaratan

- Python 3.7 atau lebih baru (disarankan Python 3.9 atau lebih baru).
- Modul Python berikut:
  - `requests`
  - Modul-modul standar seperti `concurrent.futures`, `logging`, `random`, `os`, `time` (sudah tersedia secara default di Python).

## Instalasi

### 1. Clone Repository

Clone repository ini ke dalam direktori lokal Anda:

```bash
git clone https://github.com/taufiqdayat211/mailaccess_checker.git
cd mailaccess_checker
```
2. Install Dependencies

Instal modul requests yang dibutuhkan oleh script:

`pip install requests`

3. Siapkan File Input

Buat file email_access.txt yang berisi daftar email dan password dengan format berikut:

`email1@gmail.com:password1`
`email2@yahoo.com:password2`
`email3@outlook.com:password3`

Pisahkan email dan password menggunakan tanda : (colon). Setiap baris harus berisi satu pasangan email dan password.

Cara Penggunaan

	1.	Jalankan script `check.py` dengan menggunakan Python:

`python check.py`

	2.	Anda akan diminta untuk memasukkan path ke file email_access.txt yang berisi daftar email dan password. Misalnya:

Masukkan path file email access.txt: `/path/to/email_access.txt`

	3.	Kemudian, Anda akan ditanya apakah ingin menggunakan proxy:

- Apakah kamu ingin menggunakan proxy? (y/n): y

Jika memilih ‘y’, script akan mengambil daftar proxy, mengecek proxy yang masih hidup, lalu menggunakan proxy tersebut untuk melakukan pengecekan akun email.

	4.	Script akan mulai memproses email dan mencatat hasilnya.

Contoh Output

Total proxy yang didapat: 500
Total proxy live: 50
email1@gmail.com ==> login success (domain: gmail.com)
email2@yahoo.com ==> login failed (domain: yahoo.com)
email3@outlook.com ==> login failed (domain: outlook.com)

Log File

Hasil percobaan login juga akan dicatat dalam file email_checker.log, yang mencakup status sukses/gagal serta error yang mungkin terjadi.

Fitur yang Akan Datang

	•	Dukungan untuk lebih banyak domain email.
	•	Peningkatan algoritma untuk menghindari deteksi CAPTCHA.
	•	Penggunaan API khusus untuk login email jika tersedia.

Kontribusi

Jika Anda ingin berkontribusi ke proyek ini, silakan fork repository ini, buat perubahan, dan kirimkan pull request Anda. Setiap kontribusi sangat dihargai!

	1.	Fork repository ini.
	2.	Buat branch fitur baru (git checkout -b fitur-anda).
	3.	Commit perubahan Anda (git commit -am 'Tambah fitur A').
	4.	Push ke branch (git push origin fitur-anda).
	5.	Buat pull request baru.

Lisensi

Alat ini dilisensikan di bawah lisensi MIT. Silakan lihat file LICENSE untuk informasi lebih lanjut.

### Penjelasan:

1. **Deskripsi**: Memberikan gambaran umum tentang alat, tujuannya, dan fitur utamanya.
2. **Persyaratan**: Menjelaskan versi Python yang diperlukan serta modul yang harus diinstal.
3. **Instalasi**: Menjelaskan langkah-langkah untuk meng-clone repository, menginstal dependencies, dan menyiapkan file input.
4. **Cara Penggunaan**: Langkah-langkah yang diperlukan untuk menjalankan script, termasuk contoh output dan instruksi penggunaan proxy.
5. **Fitur yang Akan Datang**: Menyertakan rencana pengembangan fitur di masa depan.
6. **Kontribusi**: Mengajak pengguna lain untuk berkontribusi ke proyek dengan mengikuti alur kontribusi GitHub.
7. **Lisensi**: Menyertakan informasi lisensi proyek.

Markdown ini akan memberikan informasi yang jelas dan lengkap untuk pengguna yang ingin menggunakan atau berkontribusi ke proyek `Email Access Checker`.
