from .auth import auth_bp
from .machines import machines_bp
from .maintenance import maintenance_bp
from .inventory import inventory_bp
from .dashboard import dashboard_bp

__all__ = ['auth_bp', 'machines_bp', 'maintenance_bp', 'inventory_bp', 'dashboard_bp']
