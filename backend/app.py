from flask import Flask
from config import Config
from extensions import mysql, jwt, cors
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from routes.jadwal import jadwal_bp
import sys

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
jwt.init_app(app)
cors.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(jadwal_bp, url_prefix='/api')

@app.route('/api/test')
def test_route():
    # Tampilkan informasi server di terminal
    port = sys.argv[2] if len(sys.argv) > 2 else '5000'
    print(f"Request diterima di port {port}")
    return {'message': f'Response dari Flask @port {port}'}

if __name__ == '__main__':
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)