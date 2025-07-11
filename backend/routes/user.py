from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
import datetime
from utils.logger import kirim_log

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
            'id_pemesanan': id_pemesanan,
            'nama_penumpang': nama,
            'kode_tiket': kode_tiket,
            'total_bayar': total_bayar
        })

    # Update kursi tersedia
    cursor.execute("UPDATE jadwal_bus SET kursi_tersedia = kursi_tersedia - %s WHERE id_jadwal = %s", (jumlah_tiket, id_jadwal))

    mysql.connection.commit()
    kirim_log("Pemesanan Tiket", f"{jumlah_tiket} tiket dipesan pada jadwal {id_jadwal}", user_id=id_user)
    cursor.close()

    return jsonify({
        'message': 'Tiket berhasil dipesan per orang',
        'data': tiket_dibuat
    }), 201

@user_bp.route('/upload-bukti', methods=['POST'])
@jwt_required()
def upload_bukti():
    data = request.get_json()
    url = data.get('url') 
    id_list = data.get('id_pemesanan_list')  # ganti dari satu ID ke list

    if not id_list or not isinstance(id_list, list):
        return jsonify({'error': 'Daftar ID pemesanan tidak valid'}), 400

    cursor = mysql.connection.cursor()
    for id_pemesanan in id_list:
        cursor.execute(
            "INSERT INTO bukti_pembayaran (id_pemesanan, file_path) VALUES (%s, %s)",
            (id_pemesanan, url)
        )

    mysql.connection.commit()
    kirim_log("Upload Bukti Pembayaran", f"Bukti diunggah untuk {len(id_list)} pemesanan", user_id=get_jwt_identity())
    cursor.close()
    return jsonify({'message': 'Bukti pembayaran berhasil diupload untuk semua pesanan'})

@user_bp.route('/etiket/<int:id_pemesanan>', methods=['GET'])
@jwt_required()
def lihat_etiket(id_pemesanan):
    user_id = int(get_jwt_identity())
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            p.id_pemesanan,         
            p.kode_tiket,          
            p.nama_penumpang,      
            j.nama_bus,            
            j.asal,                
            j.tujuan,              
            j.tanggal_berangkat,   
            j.jam_berangkat,       
            j.jam_tiba,            
            p.total_bayar        
        FROM pemesanan p
        JOIN jadwal_bus j ON p.id_jadwal = j.id_jadwal
        WHERE p.id_user = %s AND p.status_pembayaran = 'diterima' AND p.id_pemesanan = %s
        LIMIT 1
    """, (user_id, id_pemesanan))
    row = cursor.fetchone()
    cursor.close()

    if row:
        hasil = {
            'id_pemesanan': row[0],          
            'kode_tiket': row[1],             # 1. Identitas tiket
            'nama_penumpang': row[2],         # 2. Identitas penumpang
            'bus': row[3],                    # 3. Nama bus
            'asal': row[4],                   # 4. Rute: asal
            'tujuan': row[5],                 # 5. Rute: tujuan
            'tanggal': str(row[6]),          # 6. Jadwal: tanggal
            'jam_berangkat': str(row[7]),    # 7. Jadwal: jam berangkat
            'jam_tiba': str(row[8]),         # 8. Jadwal: jam tiba
            'total_bayar': float(row[9]),    # 9. Harga tiket
        }
        return jsonify(hasil)
    else:
        return jsonify({'error': 'Tiket tidak ditemukan'}), 404

@user_bp.route('/histori', methods=['GET'])
@jwt_required()
def histori():
    user_id = int(get_jwt_identity())
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            p.id_pemesanan,
            p.nama_penumpang,
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
            'nama_penumpang': row[1],
            'jumlah_tiket': row[2],
            'status': row[3],
            'total_bayar': float(row[4]),
            'tanggal_pesan': str(row[5]),
            'jadwal': {
                'tanggal': str(row[6]),
                'jam': str(row[7]),
                'asal': row[8],
                'tujuan': row[9],
                'harga_per_tiket': float(row[10])
            }
        })
    return jsonify({'riwayat': hasil})
