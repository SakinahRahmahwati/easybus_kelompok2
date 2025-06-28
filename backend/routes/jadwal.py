from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import mysql, redis_client
from middlewares.role_required import admin_required
import json

jadwal_bp = Blueprint('jadwal', __name__)

# =========================
# USER - Lihat atau Cari Jadwal Bus
# =========================
@jadwal_bp.route('/jadwal', methods=['GET'])
def get_jadwal_filtered():
    asal = request.args.get('asal')
    tujuan = request.args.get('tujuan')
    tanggal = request.args.get('tanggal')

    key = 'jadwal:all'
    cached = redis_client.get(key)
    if cached:
        semua_jadwal = json.loads(cached)
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM jadwal_bus")
        rows = cursor.fetchall()
        cursor.close()
        semua_jadwal = [{
            'id': row[0], 'nama_bus': row[1], 'asal': row[2], 'tujuan': row[3],
            'tanggal': str(row[4]), 'jam_berangkat': str(row[5]),
            'jam_tiba': str(row[6]) if row[6] else None,
            'harga': float(row[7]), 'total_kursi': row[8], 'kursi_tersedia': row[9]
        } for row in rows]
        redis_client.set(key, json.dumps(semua_jadwal), ex=600)

    hasil = [
        j for j in semua_jadwal
        if (not asal or j['asal'].lower() == asal.lower()) and
           (not tujuan or j['tujuan'].lower() == tujuan.lower()) and
           (not tanggal or j['tanggal'] == tanggal)
    ]
    return jsonify({'source': 'filtered', 'data': hasil})

# =========================
# USER - Lihat Detail Jadwal
# =========================
@jadwal_bp.route('/jadwal/<int:id>', methods=['GET'])
def get_jadwal_by_id(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM jadwal_bus WHERE id_jadwal = %s", (id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({'error': 'Jadwal tidak ditemukan'}), 404

    hasil = {
        'id': row[0], 'nama_bus': row[1], 'asal': row[2], 'tujuan': row[3],
        'tanggal': str(row[4]), 'jam_berangkat': str(row[5]),
        'jam_tiba': str(row[6]) if row[6] else None,
        'harga': float(row[7]), 'total_kursi': row[8], 'kursi_tersedia': row[9]
    }
    return jsonify({'data': hasil})

# =========================
# ADMIN - Tambah Jadwal
# =========================
@jadwal_bp.route('/admin/jadwal', methods=['POST'])
@jwt_required()
@admin_required
def tambah_jadwal():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO jadwal_bus (
            nama_bus, asal, tujuan, tanggal_berangkat,
            jam_berangkat, jam_tiba, harga, total_kursi, kursi_tersedia
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['nama_bus'], data['asal'], data['tujuan'], data['tanggal_berangkat'],
        data['jam_berangkat'], data.get('jam_tiba'), data['harga'],
        data['total_kursi'], data['kursi_tersedia']
    ))
    mysql.connection.commit()
    cursor.close()
    redis_client.delete('jadwal:all')
    return jsonify({'message': 'Jadwal berhasil ditambahkan'}), 201

# =========================
# ADMIN - Update Jadwal
# =========================
@jadwal_bp.route('/admin/jadwal/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_jadwal(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE jadwal_bus SET
            nama_bus = %s,
            asal = %s,
            tujuan = %s,
            tanggal_berangkat = %s,
            jam_berangkat = %s,
            jam_tiba = %s,
            harga = %s,
            total_kursi = %s,
            kursi_tersedia = %s
        WHERE id_jadwal = %s
    """, (
        data['nama_bus'], data['asal'], data['tujuan'],
        data['tanggal_berangkat'], data['jam_berangkat'], data.get('jam_tiba'),
        data['harga'], data['total_kursi'], data['kursi_tersedia'],
        id
    ))
    mysql.connection.commit()
    cursor.close()
    redis_client.delete('jadwal:all')
    return jsonify({'message': 'Jadwal berhasil diperbarui'}), 200

# =========================
# ADMIN - Hapus Jadwal
# =========================
@jadwal_bp.route('/admin/jadwal/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_jadwal(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM jadwal_bus WHERE id_jadwal = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    redis_client.delete('jadwal:all')
    return jsonify({'message': 'Jadwal berhasil dihapus'}), 200

# =========================
# ADMIN - Lihat Semua Jadwal
# =========================
@jadwal_bp.route('/admin/jadwal', methods=['GET'])
@jwt_required()
@admin_required
def get_all_jadwal_admin():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM jadwal_bus")
    rows = cursor.fetchall()
    cursor.close()
    hasil = [{
        'id': row[0], 'nama_bus': row[1], 'asal': row[2], 'tujuan': row[3],
        'tanggal': str(row[4]), 'jam_berangkat': str(row[5]),
        'jam_tiba': str(row[6]) if row[6] else None,
        'harga': float(row[7]), 'total_kursi': row[8], 'kursi_tersedia': row[9]
    } for row in rows]
    return jsonify({'data': hasil})
