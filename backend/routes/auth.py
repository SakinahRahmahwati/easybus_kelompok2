from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import mysql
from utils.logger import kirim_log

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_user, nama, email, password, role FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[3], password):
        token = create_access_token(identity=str(user[0]), additional_claims={
            'email': user[2],
            'role': user[4]
        })
        kirim_log("Login", f"User {user[1]} berhasil login", user_id=user[0])
        return jsonify({
            'message': 'Login berhasil',
            'token': token,
            'user': {
                'id_user': user[0],
                'nama': user[1],
                'email': user[2],
                'role': user[4]
            }
        })
    return jsonify({'error': 'Email atau password salah'}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nama = data.get('nama')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    role = data.get('role', 'customer')

    if not (nama and email and password and confirm_password):
        return jsonify({'error': 'Semua field harus diisi'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Password tidak sama'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM user WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        return jsonify({'error': 'Email sudah terdaftar'}), 400

    hashed = generate_password_hash(password)
    cursor.execute("INSERT INTO user (nama, email, password, role) VALUES (%s, %s, %s, %s)", (nama, email, hashed, role))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Registrasi berhasil'})
