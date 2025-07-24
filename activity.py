from src.models.user import db
from datetime import datetime

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    technician = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, completed, active
    machine_id = db.Column(db.String(50), db.ForeignKey('machine.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationship
    machine = db.relationship('Machine', backref=db.backref('activities', lazy=True))

    def __repr__(self):
        return f'<Activity {self.id}: {self.description}>'

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'technician': self.technician,
            'status': self.status,
            'machine_id': self.machine_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

