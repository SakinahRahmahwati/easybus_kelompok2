from flask import Flask
from config import Config
from extensions import mysql, jwt, cors
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from routes.jadwal import jadwal_bp

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
jwt.init_app(app)
cors.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(jadwal_bp)

if __name__ == '__main__':
    app.run(debug=True)