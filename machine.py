from src.models.user import db
from datetime import datetime

class Machine(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # Machine ID like "MACHINE-001"
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='operational')  # operational, warning, maintenance
    efficiency = db.Column(db.Float, default=100.0)
    temperature = db.Column(db.Float, default=25.0)
    vibration = db.Column(db.Float, default=0.5)
    last_maintenance = db.Column(db.String(50), default='2024-01-15')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Machine {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'efficiency': self.efficiency,
            'temperature': self.temperature,
            'vibration': self.vibration,
            'lastMaintenance': self.last_maintenance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

