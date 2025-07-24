from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.activity import Activity
from src.models.machine import Machine
from datetime import datetime
import random

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/', methods=['GET'])
@jwt_required()
def get_activities():
    try:
        activities = Activity.query.order_by(Activity.timestamp.desc()).all()
        return jsonify([activity.to_dict() for activity in activities]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/', methods=['POST'])
@jwt_required()
def create_activity():
    try:
        data = request.get_json()
        description = data.get('description')
        technician = data.get('technician')
        machine_id = data.get('machine_id')

        if not description or not technician:
            return jsonify({'error': 'Description and technician are required'}), 400

        # Validate machine_id if provided
        if machine_id and not Machine.query.get(machine_id):
            return jsonify({'error': 'Machine not found'}), 404

        activity = Activity(
            description=description,
            technician=technician,
            status=data.get('status', 'pending'),
            machine_id=machine_id
        )

        db.session.add(activity)
        db.session.commit()

        return jsonify(activity.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['GET'])
@jwt_required()
def get_activity(activity_id):
    try:
        activity = Activity.query.get_or_404(activity_id)
        return jsonify(activity.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    try:
        activity = Activity.query.get_or_404(activity_id)
        data = request.get_json()

        activity.description = data.get('description', activity.description)
        activity.technician = data.get('technician', activity.technician)
        activity.status = data.get('status', activity.status)
        activity.machine_id = data.get('machine_id', activity.machine_id)

        # Set completed_at if status is completed
        if data.get('status') == 'completed' and not activity.completed_at:
            activity.completed_at = datetime.utcnow()

        db.session.commit()
        return jsonify(activity.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    try:
        activity = Activity.query.get_or_404(activity_id)
        db.session.delete(activity)
        db.session.commit()
        return jsonify({'message': 'Activity deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/generate-sample', methods=['POST'])
@jwt_required()
def generate_sample_activities():
    try:
        # Get existing machines
        machines = Machine.query.all()
        machine_ids = [machine.id for machine in machines] if machines else [None]

        sample_activities = [
            {
                'description': 'Routine maintenance check on production line',
                'technician': 'Ahmed Hassan',
                'status': 'completed',
                'machine_id': random.choice(machine_ids) if machine_ids[0] else None
            },
            {
                'description': 'Replace worn belt on assembly unit',
                'technician': 'Sarah Johnson',
                'status': 'in-progress',
                'machine_id': random.choice(machine_ids) if machine_ids[0] else None
            },
            {
                'description': 'Calibrate sensors on quality control system',
                'technician': 'Mohammed Ali',
                'status': 'pending',
                'machine_id': random.choice(machine_ids) if machine_ids[0] else None
            },
            {
                'description': 'Oil change and lubrication service',
                'technician': 'Lisa Chen',
                'status': 'completed',
                'machine_id': random.choice(machine_ids) if machine_ids[0] else None
            },
            {
                'description': 'Emergency repair on packaging unit',
                'technician': 'David Rodriguez',
                'status': 'active',
                'machine_id': random.choice(machine_ids) if machine_ids[0] else None
            }
        ]

        created_activities = []
        for activity_data in sample_activities:
            activity = Activity(
                description=activity_data['description'],
                technician=activity_data['technician'],
                status=activity_data['status'],
                machine_id=activity_data['machine_id']
            )
            
            # Set completed_at for completed activities
            if activity_data['status'] == 'completed':
                activity.completed_at = datetime.utcnow()
            
            db.session.add(activity)
            created_activities.append(activity_data['description'])

        db.session.commit()
        return jsonify({
            'message': f'Created {len(created_activities)} sample activities',
            'activities': created_activities
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

