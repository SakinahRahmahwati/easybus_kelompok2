from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
@jwt_required()
def list_user():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_user, nama, email, password, role FROM user")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{ 'id_user': r[0], 'nama': r[1], 'email': r[2], 'password': r[3], 'role': r[4]} for r in rows])

@user_bp.route('/pemesanan', methods=['POST'])
@jwt_required()
def pesan_tiket():
    data = request.get_json()
    id_user = int(get_jwt_identity())
    id_jadwal = data.get('id_jadwal')
    nama_penumpang_list = data.get('nama_penumpang')  # array

    if not id_jadwal or not nama_penumpang_list or not isinstance(nama_penumpang_list, list):
        return jsonify({'error': 'Data tidak lengkap atau format salah'}), 400

    jumlah_tiket = len(nama_penumpang_list)

    cursor = mysql.connection.cursor()

    # Cek jadwal
    cursor.execute("SELECT harga, kursi_tersedia FROM jadwal_bus WHERE id_jadwal = %s", (id_jadwal,))
    jadwal = cursor.fetchone()
    if not jadwal:
        cursor.close()
        return jsonify({'error': 'Jadwal tidak ditemukan'}), 404

    harga_satuan = float(jadwal[0])
    kursi_tersedia = int(jadwal[1])

    if kursi_tersedia < jumlah_tiket:
        cursor.close()
        return jsonify({'error': 'Jumlah kursi tidak mencukupi'}), 400

    tiket_dibuat = []

    for nama in nama_penumpang_list:
        total_bayar = harga_satuan  # selalu 1 tiket per baris
        cursor.execute("""
            INSERT INTO pemesanan (id_user, id_jadwal, nama_penumpang, jumlah_tiket, total_bayar)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_user, id_jadwal, nama, 1, total_bayar))

        id_pemesanan = cursor.lastrowid
        kode_tiket = f"ETK-{datetime.datetime.now().strftime('%Y%m%d')}-{id_pemesanan:04d}"

        cursor.execute("UPDATE pemesanan SET kode_tiket = %s WHERE id_pemesanan = %s", (kode_tiket, id_pemesanan))

        tiket_dibuat.append({
            'nama_penumpang': nama,
            'kode_tiket': kode_tiket,
            'total_bayar': total_bayar
        })

    # Update kursi tersedia
    cursor.execute("UPDATE jadwal_bus SET kursi_tersedia = kursi_tersedia - %s WHERE id_jadwal = %s", (jumlah_tiket, id_jadwal))

    mysql.connection.commit()
    cursor.close()

    return jsonify({
        'message': 'Tiket berhasil dipesan per orang',
        'data': tiket_dibuat
    }), 201

@user_bp.route('/upload-bukti', methods=['POST'])
@jwt_required()
def upload_bukti():
    data = request.get_json()
    url = data.get('url')  # contoh: nama file atau path bukti
    id_pemesanan = data.get('id_pemesanan')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO bukti_pembayaran (id_pemesanan, file_path) VALUES (%s, %s)", (id_pemesanan, url))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Bukti pembayaran berhasil diupload'})

@user_bp.route('/etiket', methods=['GET'])
@jwt_required()
def lihat_etiket():
    user_id = int(get_jwt_identity())
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            p.id_pemesanan,
            p.kode_tiket,
            p.nama_penumpang,
            p.total_bayar,
            j.nama_bus,
            j.asal,
            j.tujuan,
            j.tanggal_berangkat,
            j.jam_berangkat
        FROM pemesanan p
        JOIN jadwal_bus j ON p.id_jadwal = j.id_jadwal
        WHERE p.id_user = %s AND p.status_pembayaran = 'diterima'
        ORDER BY p.created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()

    hasil = []
    for row in rows:
        hasil.append({
            'id_pemesanan': row[0],
            'kode_tiket': row[1],
            'nama_penumpang': row[2],
            'total_bayar': float(row[3]),
            'bus': row[4],
            'asal': row[5],
            'tujuan': row[6],
            'tanggal': str(row[7]),
            'jam_berangkat': str(row[8])
        })

    return jsonify({'e_tiket': hasil})


@user_bp.route('/histori', methods=['GET'])
@jwt_required()
def histori():
    user_id = int(get_jwt_identity())
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            p.id_pemesanan,
            p.jumlah_tiket,
            p.status_pembayaran,
            p.total_bayar,
            p.created_at,
            j.tanggal_berangkat,
            j.jam_berangkat,
            j.asal,
            j.tujuan,
            j.harga
        FROM pemesanan p
        JOIN jadwal_bus j ON p.id_jadwal = j.id_jadwal
        WHERE p.id_user = %s
        ORDER BY p.created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()

    hasil = []
    for row in rows:
        hasil.append({
            'id_pemesanan': row[0],
            'jumlah_tiket': row[1],
            'status': row[2],
            'total_bayar': float(row[3]),
            'tanggal_pesan': str(row[4]),
            'jadwal': {
                'tanggal': str(row[5]),
                'jam': str(row[6]),
                'asal': row[7],
                'tujuan': row[8],
                'harga_per_tiket': float(row[9])
            }
        })
    return jsonify({'riwayat': hasil})
