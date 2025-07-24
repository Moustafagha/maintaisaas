from src.models.user import db
from datetime import datetime

class PredictiveData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(50), db.ForeignKey('machine.id'), nullable=False)
    failure_probability = db.Column(db.Float, default=0.0)
    recommended_maintenance = db.Column(db.Integer, default=30)  # days
    cost_savings = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    machine = db.relationship('Machine', backref=db.backref('predictive_data', lazy=True))

    def __repr__(self):
        return f'<PredictiveData for {self.machine_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'machine_id': self.machine_id,
            'failureProbability': self.failure_probability,
            'recommendedMaintenance': self.recommended_maintenance,
            'costSavings': self.cost_savings,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

