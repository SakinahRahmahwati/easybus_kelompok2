from flask_mysqldb import MySQL
from flask_cors import CORS
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from functools import wraps
import redis
import json

app = Flask(__name__)

# Konfigurasi CORS untuk mengizinkan akses dari frontend (localhost:8080)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'easybus'
app.config['MYSQL_SSL_DISABLED'] = True

# Konfigurasi JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Konfigurasi Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

mysql = MySQL(app)

# Simpan blacklist token
blacklist = set()

# Middleware Role Admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Akses hanya untuk admin'}), 403
        return fn(*args, **kwargs)
    return wrapper

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

@app.route('/')
def root():
    return redirect('/login')

@app.route("/token", methods=["GET"])
def get_token():
    token = create_access_token(identity="1")  # atau identity=str(1)
    return jsonify(access_token=token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(message="Access granted")

#====================================================LOGIN DAN REGISTRASI===========================================#
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email dan password harus diisi'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_user, nama, email, password, role FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            # Buat token akses
            access_token = create_access_token(
                identity=str(user[0]),
                additional_claims={
                    'email': user[2],
                    'role': user[4]
                }
            )
            return jsonify({
                'message': 'Login berhasil',
                'token': access_token,
                'user': {
                    'id_user': user[0],
                    'nama': user[1],
                    'email': user[2],
                    'role': user[4]
                }
            }), 200
        else:
            return jsonify({'error': 'Email atau password salah'}), 401
    return jsonify({'error': 'Request harus dalam format JSON'}), 400

@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
        
        nama = data.get('nama')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        role = data.get('role', 'customer')  # Default role to 'customer'

        # Validasi jika ada field yang kosong
        if not (nama and email and password and confirm_password):
            return jsonify({'error': 'Nama, email, password, dan konfirmasi password harus diisi'}), 400

        # Validasi jika password dan konfirmasi password tidak sama
        if password != confirm_password:
            return jsonify({'error': 'Password dan konfirmasi password harus sama'}), 400

        # Periksa apakah email sudah terdaftar
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            return jsonify({'error': 'Email sudah terdaftar'}), 400

        # Hash password sebelum disimpan
        hashed_password = generate_password_hash(password)

        # Insert data ke database
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO user (nama, email, password, role) VALUES (%s, %s, %s, %s)",
            (nama, email, hashed_password, role)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User berhasil didaftarkan, silakan login!'}), 201

    return jsonify({'error': 'Request harus dalam format JSON'}), 400

#============================================================PENUMPANG & ADMIN===================================================#
@app.route('/jadwal', methods=['GET'])
def get_jadwal():
    key = 'jadwal:all'
    cached = redis_client.get(key)
    if cached:
        return jsonify({'source': 'redis', 'data': json.loads(cached)})

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM jadwal_bus")
    rows = cursor.fetchall()
    cursor.close()

    hasil = []
    for row in rows:
        hasil.append({
            'id': row[0],
            'nama_bus': row[1],
            'asal': row[2],
            'tujuan': row[3],
            'tanggal': str(row[4]),
            'jam_berangkat': str(row[5]),
            'jam_tiba': str(row[6]) if row[6] else None,
            'harga': float(row[7]),
            'total_kursi': row[8],
            'kursi_tersedia': row[9]
        })

    redis_client.set(key, json.dumps(hasil), ex=600)
    return jsonify({'source': 'mysql', 'data': hasil})

#============================================================PENUMPANG===================================================#
@app.route('/user', methods=['GET'])
def list_user():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_user, nama, email, password, role FROM user")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        user_data = {
            'id_user' : row[0],
            'nama': row[1],
            'email': row[2],
            'password': row[3],
            'role': row[4]
        }
        result.append(user_data)

    cursor.close()
    return jsonify(result), 200 

@app.route('/pemesanan', methods=['POST'])
@jwt_required()
def pesan_tiket():
    data = request.get_json()
    id_jadwal = data.get('id_jadwal')
    jumlah_tiket = data.get('jumlah_tiket')
    id_user = int(get_jwt_identity())


    if not id_jadwal or not jumlah_tiket:
        return jsonify({'error': 'ID jadwal dan jumlah tiket wajib diisi'}), 400

    cursor = mysql.connection.cursor()

    # Periksa jadwal valid
    cursor.execute("SELECT jumlah_kursi FROM jadwal WHERE id_jadwal = %s", (id_jadwal,))
    jadwal = cursor.fetchone()
    if not jadwal:
        cursor.close()
        return jsonify({'error': 'Jadwal tidak ditemukan'}), 404

    # Cek ketersediaan kursi
    sisa_kursi = jadwal[0]
    if sisa_kursi < jumlah_tiket:
        cursor.close()
        return jsonify({'error': 'Jumlah kursi tidak mencukupi'}), 400

    # Simpan pemesanan
    cursor.execute("""
        INSERT INTO pemesanan (id_user, id_jadwal, jumlah_tiket)
        VALUES (%s, %s, %s)
    """, (id_user, id_jadwal, jumlah_tiket))

    # Kurangi jumlah kursi
    cursor.execute("""
        UPDATE jadwal SET jumlah_kursi = jumlah_kursi - %s WHERE id_jadwal = %s
    """, (jumlah_tiket, id_jadwal))

    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Pemesanan berhasil'}), 201


@app.route('/upload-bukti', methods=['POST'])
@jwt_required()
def upload_bukti():
    data = request.get_json()
    url = data.get('url')
    id_pemesanan = data.get('id_pemesanan')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE pemesanan SET bukti_url = %s WHERE id = %s", (url, id_pemesanan))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Bukti upload berhasil'})

@app.route('/histori', methods=['GET'])
@jwt_required()
def histori():
    user_id = int(get_jwt_identity())
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            p.id_pemesanan,
            p.jumlah_tiket,
            p.status,
            p.bukti_url,
            p.tanggal_pesan,
            j.tanggal,
            j.jam,
            j.asal,
            j.tujuan,
            j.harga
        FROM pemesanan p
        JOIN jadwal j ON p.id_jadwal = j.id_jadwal
        WHERE p.id_user = %s
        ORDER BY p.tanggal_pesan DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    cursor.close()

    hasil = []
    for row in rows:
        hasil.append({
            'id_pemesanan': row[0],
            'jumlah_tiket': row[1],
            'status': row[2],
            'bukti_url': row[3],
            'tanggal_pesan': str(row[4]),
            'jadwal': {
                'tanggal': str(row[5]),
                'jam': str(row[6]),
                'asal': row[7],
                'tujuan': row[8],
                'harga': float(row[9])
            }
        })

    return jsonify({'riwayat': hasil}), 200

#============================================================ADMIN===================================================#
@app.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def dashboard_summary():
    cursor = mysql.connection.cursor()

    # Jumlah semua user
    cursor.execute("SELECT COUNT(*) FROM user")
    total_user = cursor.fetchone()[0]

    # Jumlah customer (role = 'customer')
    cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'customer'")
    total_customer = cursor.fetchone()[0]

    # Jumlah jadwal (tiket)
    cursor.execute("SELECT COUNT(*) FROM jadwal_bus")
    total_jadwal = cursor.fetchone()[0]

    # Jumlah booking (pemesanan)
    cursor.execute("SELECT COUNT(*) FROM pemesanan")
    total_pemesanan = cursor.fetchone()[0]

    cursor.close()

    return jsonify({
        'total_user': total_user,
        'total_customer': total_customer,
        'total_jadwal': total_jadwal,
        'total_pemesanan': total_pemesanan
    }), 200

@app.route('/add-user', methods=['POST'])
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
    
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
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

@app.route('/jadwal', methods=['POST'])
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
            data['jam_berangkat'], data['jam_tiba'], data['harga'],
            data['total_kursi'], data['kursi_tersedia']
        ))
    mysql.connection.commit()
    cursor.close()
    redis_client.delete('jadwal:all')
    return jsonify({'message': 'Jadwal berhasil ditambahkan'}), 201

@app.route('/jadwal/<int:id>', methods=['PUT'])
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

@app.route('/jadwal/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_jadwal(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM jadwal_bus WHERE id_jadwal = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    redis_client.delete('jadwal:all')
    return jsonify({'message': 'Jadwal berhasil dihapus'}), 200

@app.route('/verifikasi/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def verifikasi(id):
    data = request.get_json()
    status = data.get('status')  # 'diterima' atau 'ditolak'

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE pemesanan SET status = %s WHERE id = %s", (status, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Verifikasi berhasil'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)