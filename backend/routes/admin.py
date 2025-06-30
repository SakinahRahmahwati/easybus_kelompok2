from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
from middlewares.role_required import admin_required
from werkzeug.security import generate_password_hash
from utils.logger import kirim_log

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    total_user = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'customer'")
    total_customer = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jadwal_bus")
    total_jadwal = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pemesanan")
    total_pemesanan = cursor.fetchone()[0]
    cursor.close()

    return jsonify({
        'total_user': total_user,
        'total_customer': total_customer,
        'total_jadwal': total_jadwal,
        'total_pemesanan': total_pemesanan
    })

@admin_bp.route('/admin/pemesanan', methods=['GET'])
@jwt_required()
@admin_required
def semua_pemesanan():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT p.id_pemesanan, u.nama, p.nama_penumpang, j.nama_bus, j.tanggal_berangkat,
               p.total_bayar, p.status_pembayaran, p.kode_tiket
        FROM pemesanan p
        JOIN user u ON p.id_user = u.id_user
        JOIN jadwal_bus j ON p.id_jadwal = j.id_jadwal
        ORDER BY p.created_at DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    hasil = []
    for row in rows:
        hasil.append({
            'id_pemesanan': row[0],
            'nama_user': row[1],
            'nama_penumpang': row[2],
            'bus': row[3],
            'tanggal': str(row[4]),
            'total_bayar': float(row[5]),
            'status': row[6],
            'kode_tiket': row[7]
        })
    return jsonify({'data': hasil})

@admin_bp.route('/admin/bukti', methods=['GET'])
@jwt_required()
@admin_required
def semua_bukti_pembayaran():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT b.id_pemesanan, p.nama_penumpang, p.kode_tiket, b.file_path, p.status_pembayaran
        FROM bukti_pembayaran b
        JOIN pemesanan p ON b.id_pemesanan = p.id_pemesanan
        ORDER BY b.id_pemesanan DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    hasil = []
    for row in rows:
        hasil.append({
            'id_pemesanan': row[0],
            'nama_penumpang': row[1],
            'kode_tiket': row[2],
            'file_url': row[3],
            'status_pembayaran': row[4]
        })
    return jsonify({'data': hasil})

@admin_bp.route('/verifikasi/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def verifikasi(id):
    data = request.get_json()
    status = data.get('status')  # 'diterima' atau 'ditolak'
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE pemesanan SET status_pembayaran = %s WHERE id_pemesanan = %s", (status, id))
    kirim_log("Verifikasi Pembayaran", f"Status pemesanan ID {id} diubah menjadi {status}", user_id=get_jwt_identity())
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Verifikasi berhasil'})

@admin_bp.route('/admin/laporan', methods=['GET'])
@jwt_required()
@admin_required
def laporan_dashboard():
    cursor = mysql.connection.cursor()

    # Total pemesanan
    cursor.execute("SELECT COUNT(*) FROM pemesanan")
    total_pemesanan = cursor.fetchone()[0]

    # Tiket diterima
    cursor.execute("SELECT COUNT(*) FROM pemesanan WHERE status_pembayaran = 'diterima'")
    tiket_diterima = cursor.fetchone()[0]

    # Total pengguna
    cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'user'")
    total_user = cursor.fetchone()[0]

    # Total pendapatan
    cursor.execute("SELECT SUM(total_bayar) FROM pemesanan WHERE status_pembayaran = 'diterima'")
    pendapatan = cursor.fetchone()[0] or 0

    cursor.close()

    return jsonify({
        'total_pemesanan': total_pemesanan,
        'tiket_diterima': tiket_diterima,
        'total_user': total_user,
        'pendapatan': pendapatan
    })

@admin_bp.route('/add-user', methods=['POST'])
@jwt_required()
@admin_required
def tambah_user():
    if request.is_json:
        data = request.get_json()

        nama = data.get('nama')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not (nama and email and password and role):
            return jsonify({'error': 'Semua field harus diisi'}), 400

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO user (nama, email, password, role) VALUES (%s, %s, %s, %s)",
            (nama, email, hashed_password, role)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data user berhasil ditambahkan!'})
    
@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_user FROM user WHERE id_user = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            return jsonify({'error': 'User tidak ditemukan'}), 404
        
        cursor.execute("DELETE FROM user WHERE id_user = %s", (user_id,))
        mysql.connection.commit()
        kirim_log("Hapus User", f"User ID {user_id} berhasil dihapus", user_id=get_jwt_identity())
        cursor.close()

        return jsonify({'message': 'User berhasil dihapus'}), 200
    except Exception as e:
        kirim_log("Error Delete User", str(e), user_id=get_jwt_identity())
        return jsonify({'error': f'Gagal menghapus user: {str(e)}'}), 500