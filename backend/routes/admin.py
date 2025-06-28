from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import mysql
from middlewares.role_required import admin_required
from werkzeug.security import generate_password_hash

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

@admin_bp.route('/verifikasi/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def verifikasi(id):
    data = request.get_json()
    status = data.get('status')  # 'diterima' atau 'ditolak'
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE pemesanan SET status_pembayaran = %s WHERE id_pemesanan = %s", (status, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Verifikasi berhasil'})

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
        cursor.close()

        return jsonify({'message': 'User berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': f'Gagal menghapus user: {str(e)}'}), 500