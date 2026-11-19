
import streamlit as st
import mysql.connector
import pandas as pd

# ==================================
# 1. KONEKSI DATABASE
# ==================================

def koneksi():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_kampus2"
    )
    return db


# ==================================
# 2. MENU APLIKASI
# ==================================

st.title("Aplikasi Data Mahasiswa")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Tambah Data",
        "Data Mahasiswa",
        "Cari Mahasiswa",
        "Kelola Data Mahasiswa",
        "Hapus Data Mahasiswa"
    ]
)


# ==================================
# 3. TAMBAH DATA MAHASISWA
# ==================================

if menu == "Tambah Data":

    st.subheader("Tambah Data Mahasiswa")

    nim = st.text_input("NIM")
    nama = st.text_input("Nama Mahasiswa")

    ipk = st.number_input(
        "IPK",
        min_value=0.0,
        max_value=4.0,
        step=0.01
    )

    semester = st.number_input(
        "Semester",
        min_value=1,
        max_value=14,
        step=1
    )

    prodi = st.selectbox(
        "Program Studi",
        [
            "Sistem Informasi",
            "Teknik Informatika",
            "Teknologi Informasi"
        ]
    )

    if st.button("Simpan Data"):

        if nim == "" or nama == "":
            st.warning("NIM dan Nama harus diisi!")

        else:
            db = koneksi()
            cursor = db.cursor()

            sql = """
                INSERT INTO mahasiswa
                (nim, nama, ipk, semester, prodi)
                VALUES (%s, %s, %s, %s, %s)
            """

            nilai = (nim, nama, ipk, semester, prodi)

            cursor.execute(sql, nilai)
            db.commit()

            cursor.close()
            db.close()

            st.success("Data berhasil disimpan!")


# ==================================
# 4. MENAMPILKAN DATA MAHASISWA
# ==================================

elif menu == "Data Mahasiswa":

    st.subheader("Daftar Mahasiswa")

    db = koneksi()

    query = "SELECT * FROM mahasiswa"

    data = pd.read_sql(query, db)

    st.dataframe(data, use_container_width=True)

    db.close()


# ==================================
# 5. CARI DATA MAHASISWA
# ==================================

elif menu == "Cari Mahasiswa":

    st.subheader("Cari Data Mahasiswa")

    cari = st.text_input("Masukkan NIM atau Nama Mahasiswa")

    if st.button("Cari Data"):

        db = koneksi()
        cursor = db.cursor()

        sql = """
            SELECT * FROM mahasiswa
            WHERE nim LIKE %s OR nama LIKE %s
        """

        nilai = ("%" + cari + "%", "%" + cari + "%")

        cursor.execute(sql, nilai)

        hasil = cursor.fetchall()

        if hasil:

            data = pd.DataFrame(
                hasil,
                columns=[i[0] for i in cursor.description]
            )

            st.success("Data berhasil ditemukan!")

            st.dataframe(data, use_container_width=True)

        else:
            st.warning("Data mahasiswa tidak ditemukan.")

        cursor.close()
        db.close()


# ==================================
# 6. EDIT DATA MAHASISWA
# ==================================

elif menu == "Kelola Data Mahasiswa":

    st.subheader("Edit Data Mahasiswa")

    db = koneksi()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM mahasiswa")

    data = cursor.fetchall()

    if data:

        pilihan = st.selectbox(
            "Pilih Mahasiswa",
            data,
            format_func=lambda x: str(x[1]) + " - " + str(x[2])
        )

        id_mahasiswa = pilihan[0]

        st.write("### Form Edit Data")

        nim = st.text_input("NIM", value=pilihan[1])

        nama = st.text_input("Nama", value=pilihan[2])

        ipk = st.number_input(
            "IPK",
            min_value=0.0,
            max_value=4.0,
            value=float(pilihan[3]),
            step=0.01
        )

        semester = st.number_input(
            "Semester",
            min_value=1,
            max_value=14,
            value=int(pilihan[4]),
            step=1
        )

        daftar_prodi = [
            "Sistem Informasi",
            "Teknik Informatika",
            "Teknologi Informasi"
        ]

        prodi_lama = pilihan[5]

        if prodi_lama not in daftar_prodi:
            daftar_prodi.append(prodi_lama)

        prodi = st.selectbox(
            "Program Studi",
            daftar_prodi,
            index=daftar_prodi.index(prodi_lama)
        )

        if st.button("Update Data"):

            sql = """
                UPDATE mahasiswa
                SET nim=%s,
                    nama=%s,
                    ipk=%s,
                    semester=%s,
                    prodi=%s
                WHERE id=%s
            """

            nilai = (
                nim,
                nama,
                ipk,
                semester,
                prodi,
                id_mahasiswa
            )

            cursor.execute(sql, nilai)

            db.commit()

            st.success("Data mahasiswa berhasil diperbarui!")

    else:
        st.warning("Belum ada data mahasiswa.")

    cursor.close()
    db.close()


# ==================================
# 7. HAPUS DATA MAHASISWA
# ==================================

elif menu == "Hapus Data Mahasiswa":

    st.subheader("Hapus Data Mahasiswa")

    db = koneksi()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM mahasiswa")

    data = cursor.fetchall()

    if data:

        pilihan = st.selectbox(
            "Pilih Mahasiswa yang akan dihapus",
            data,
            format_func=lambda x: str(x[1]) + " - " + str(x[2])
        )

        st.write("Data yang akan dihapus:")

        st.write("NIM:", pilihan[1])

        st.write("Nama:", pilihan[2])

        if st.button("Hapus Data"):

            sql = "DELETE FROM mahasiswa WHERE id=%s"

            cursor.execute(sql, (pilihan[0],))

            db.commit()

            st.success("Data mahasiswa berhasil dihapus!")

    else:
        st.warning("Belum ada data mahasiswa.")

    cursor.close()
    db.close()
