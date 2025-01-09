# SDG 4.0


## cheat code  mongosh
docker exec -it mongodb mongosh
show dbs
use `db_name`
show collections
db.`collection_name`.find()
<!-- connect to mongodb in docker -->
docker exec -it 

Document based
CRUD
Dashboard

## Replacement

1. Add , in between province name and data
```regex
^([^\d]+)\s(.*)$
```

```
$1,$2
```
1. replace ` ` with `,` 
2. replace `\n` with `,\n` 



## SDG 4.0 Target
4.1.1.(a)
Proporsi anak-anak dan remaja di: (a) kelas 5 (b) kelas 8, dan (c) usia 15 tahun yang mencapai setidaknya tingkat kemahiran minimum dalam: (i) membaca, (ii) matematika.
4.1.2*
Tingkat penyelesaian pendidikan jenjang SD/sederajat, SMP/sederajat, dan SMA/sederajat.
4.1.2.(a)
Angka anak tidak sekolah jenjang PAUD, SD/sederajat, SMP/sederajat, dan SMA/sederajat.
4.2.1*
Proporsi anak usia 24-59 bulan yang berkembang dengan baik dalam bidang kesehatan, pembelajaran, dan psikososial, menurut jenis kelamin.
4.2.2*
Tingkat partisipasi dalam pembelajaran yang teroganisir (satu tahun sebelum usia sekolah dasar), menurut jenis kelamin.
4.3.1*
Tingkat partisipasi remaja dan dewasa dalam pendidikan dan pelatihan formal dan non formal dalam 12 bulan terakhir, menurut jenis kelamin.
4.3.1.(a)
Angka Partisipasi Kasar (APK) Perguruan Tinggi (PT).
4.4.1.(a)
Proporsi remaja (usia 15-24 tahun) dan dewasa (usia 15-59 tahun) dengan keterampilan teknologi informasi dan komunikasi (TIK).
4.5.1*
Rasio Angka Partisipasi Murni (APM) pada tingkat SD/sederajat, dan (ii) Rasio Angka Partisipasi Kasar (APK) pada tingkat SMP/sederajat, SMA/SMK/sederajat, dan Perguruan Tinggi untuk (a) perempuan/ laki-laki, (b) pedesaan/ perkotaan, (c) kuintil terbawah/teratas, (d) disabilitas/tanpa disabilitas.
4.6.1.(a)
Persentase angka melek aksara penduduk umur ≥ 15 tahun.
4.a.1*
Proporsi sekolah dengan akses ke: (a) listrik (b) internet untuk tujuan pengajaran, (c) komputer untuk tujuan pengajaran, (d) air minum layak, (e) fasilitas sanitasi dasar per jenis kelamin, (f) fasilitas cuci tangan (terdiri air, sanitasi, dan higienis bagi semua (WASH).
4.7.1*
Pengarusutamaan (i) pendidikan kewargaan global, dan (ii) pendidikan pembangunan berkelanjutan termasuk kesetaraan gender dan hak asasi manusia yang tercantum dalam (a) kebijakan pendidikan, (b) kurikulum pendidikan, (c) pelatihan guru, (d) asesmen siswa, pada jenjang pendidikan dasar dan menengah.
4.a.1.(a)
Persentase siswa yang mengalami perundungan dalam 12 bulan terakhir.
4.b.1*
Jumlah bantuan resmi Pemerintah Indonesia kepada mahasiswa asing penerima beasiswa kemitraan negara berkembang.
4.c.1*
Persentase guru yang memenuhi kualifikasi sesuai dengan standar nasional menurut jenjang pendidikan.

source: https://sdgs.bappenas.go.id/metadata-indikator-sdgs/

```
uvicorn app.main:app --reload
```

TODO:
1. Change province name to lower case, delete collections and reenter it
2. Change the name in the dashboard_metal.html into the data. 
3. Create CRUD to enter the data
4. Add province to the user
5. When entering add national average? on input find same year + indicator type, then calculate the average