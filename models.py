from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """Modelo de Usuario - Mecánico o Supervisor"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'mechanic' o 'supervisor'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    maintenance_records = db.relationship('MaintenanceRecord', backref='mechanic', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Machine(db.Model):
    """Modelo de Máquina"""
    __tablename__ = 'machines'
    
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(100), unique=True, nullable=False)
    machine_type = db.Column(db.String(100), nullable=False)
    production_line = db.Column(db.Integer, nullable=False)  # 1-25
    location = db.Column(db.String(200), nullable=False)  # Ubicación actual
    status = db.Column(db.String(50), default='active')  # active, warehouse, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    maintenance_records = db.relationship('MaintenanceRecord', backref='machine', lazy=True)
    inventory = db.relationship('MachineInventory', backref='machine', uselist=False)
    warehouse = db.relationship('Warehouse', backref='machine', uselist=False)
    
    def __repr__(self):
        return f'<Machine {self.serial}>'


class MaintenanceRecord(db.Model):
    """Modelo de Registro de Mantenimiento"""
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    defect = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='in_progress')  # in_progress, completed, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_duration(self):
        """Calcula la duración del mantenimiento en minutos"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None
    
    def __repr__(self):
        return f'<MaintenanceRecord {self.id}>'


class MachineInventory(db.Model):
    """Modelo de Inventario de Máquinas"""
    __tablename__ = 'machine_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False, unique=True)
    serial = db.Column(db.String(100), nullable=False)
    machine_type = db.Column(db.String(100), nullable=False)
    production_line = db.Column(db.Integer, nullable=False)
    current_location = db.Column(db.String(200), nullable=False)
    total_maintenance_count = db.Column(db.Integer, default=0)
    last_maintenance = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MachineInventory {self.serial}>'


class Warehouse(db.Model):
    """Modelo de Bodega de Máquinas"""
    __tablename__ = 'warehouse'
    
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False, unique=True)
    serial = db.Column(db.String(100), nullable=False)
    machine_type = db.Column(db.String(100), nullable=False)
    warehouse_location = db.Column(db.String(200), nullable=False)  # Ubicación en bodega
    reason = db.Column(db.String(200), nullable=False)  # Razón del almacenamiento
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    exit_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Warehouse {self.serial}>'
