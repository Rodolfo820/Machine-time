from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///machine_time.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Crear tablas
    with app.app_context():
        from models import User, Machine, MaintenanceRecord, MachineInventory, Warehouse
        db.create_all()
    
    # Registrar blueprints
    from routes import auth_bp, machines_bp, maintenance_bp, inventory_bp, dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(machines_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(dashboard_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
