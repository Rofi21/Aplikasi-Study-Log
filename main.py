from datetime import date, datetime, timedelta

catatan = []

def tambah_catatan():
    mapel = input("Masukkan mata pelajaran: ").strip()
    topik = input("Masukkan topik: ").strip()

    while True:
        durasi_input = input("Masukkan durasi belajar (menit): ").strip()
        try:
            durasi = int(durasi_input)
            if durasi <= 0:
                print("Durasi harus lebih dari 0. Coba lagi.")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat untuk durasi (mis. 30). Coba lagi.")

    catatan_baru = {
        "mapel": mapel,
        "topik": topik,
        "durasi": durasi,
        "tanggal": date.today().isoformat(),
    }
    catatan.append(catatan_baru)
    print("Catatan berhasil ditambahkan!")

def lihat_catatan():
    if not catatan:
        print("Belum ada catatan belajar.")
        return

    # Tentukan lebar kolom berdasarkan isi terpanjang. Gunakan str() untuk
    # aman jika nilai None atau non-string disimpan.
    mapel_width = max(len(str(c.get("mapel", ""))) for c in catatan)
    topik_width = max(len(str(c.get("topik", ""))) for c in catatan)
    mapel_width = max(mapel_width, len("Mata Pelajaran"))
    topik_width = max(topik_width, len("Topik"))

    print("\nDaftar Catatan Belajar:")
    header = f"{'No':<3} {'Mata Pelajaran':<{mapel_width}}  {'Topik':<{topik_width}}  Durasi"
    print(header)
    print('-' * len(header))

    for i, c in enumerate(catatan, start=1):
        mapel = str(c.get('mapel', ''))
        topik = str(c.get('topik', ''))
        durasi = c.get('durasi', 0)
        print(f"{i:<3} {mapel:<{mapel_width}}  {topik:<{topik_width}}  {durasi} menit")

def total_waktu():
    total = sum(item.get("durasi", 0) for item in catatan)
    print(f"Total waktu belajar: {total} menit")

def ringkasan_mingguan():
    today = date.today()
    week_start = today - timedelta(days=6)

    # Pilih catatan yang termasuk rentang 7 hari terakhir.
    minggu = []
    for item in catatan:
        tstr = item.get('tanggal')
        tdate = None
        if tstr:
            try:
                tdate = datetime.strptime(tstr, "%Y-%m-%d").date()
            except Exception:
                tdate = None

        # Jika tidak ada tanggal tersimpan, anggap termasuk (kompatibilitas)
        if tdate is None or (week_start <= tdate <= today):
            minggu.append(item)

    if not minggu:
        print("Tidak ada catatan dalam 7 hari terakhir.")
        return

    total_menit = sum(i.get('durasi', 0) for i in minggu)
    sesi = len(minggu)

    per_mapel = {}
    per_topik = {}
    for i in minggu:
        m = i.get('mapel', 'Lainnya')
        t = i.get('topik', 'Umum')
        d = i.get('durasi', 0)
        per_mapel[m] = per_mapel.get(m, 0) + d
        per_topik[t] = per_topik.get(t, 0) + d

    print(f"\nRingkasan Mingguan ({week_start.isoformat()} sampai {today.isoformat()}):")
    print(f"- Jumlah sesi: {sesi}")
    print(f"- Total waktu: {total_menit} menit")

    print("\nWaktu per Mata Pelajaran:")
    for m, menit in sorted(per_mapel.items(), key=lambda x: x[1], reverse=True):
        print(f"- {m}: {menit} menit")

    print("\nTopik teratas (berdasarkan durasi):")
    top_topics = sorted(per_topik.items(), key=lambda x: x[1], reverse=True)[:5]
    for t, menit in top_topics:
        print(f"- {t}: {menit} menit")

def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Keluar")
    print("5. Ringkasan mingguan")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_catatan()
    elif pilihan == "2":
        lihat_catatan()
    elif pilihan == "3":
        total_waktu()
    elif pilihan == "5":
        ringkasan_mingguan()
    elif pilihan == "4":
        print("Terima kasih, terus semangat belajar!")
        break
    else:
        print("Pilihan tidak valid")