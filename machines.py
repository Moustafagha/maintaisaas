from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.machine import Machine
import random

machines_bp = Blueprint('machines', __name__)

@machines_bp.route('/', methods=['GET'])
@jwt_required()
def get_machines():
    try:
        machines = Machine.query.all()
        return jsonify([machine.to_dict() for machine in machines]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@machines_bp.route('/', methods=['POST'])
@jwt_required()
def create_machine():
    try:
        data = request.get_json()
        machine_id = data.get('id')
        name = data.get('name')

        if not machine_id or not name:
            return jsonify({'error': 'Machine ID and name are required'}), 400

        # Check if machine already exists
        if Machine.query.get(machine_id):
            return jsonify({'error': 'Machine ID already exists'}), 400

        machine = Machine(
            id=machine_id,
            name=name,
            status=data.get('status', 'operational'),
            efficiency=data.get('efficiency', 100.0),
            temperature=data.get('temperature', 25.0),
            vibration=data.get('vibration', 0.5),
            last_maintenance=data.get('last_maintenance', '2024-01-15')
        )

        db.session.add(machine)
        db.session.commit()

        return jsonify(machine.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@machines_bp.route('/<machine_id>', methods=['GET'])
@jwt_required()
def get_machine(machine_id):
    try:
        machine = Machine.query.get_or_404(machine_id)
        return jsonify(machine.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@machines_bp.route('/<machine_id>', methods=['PUT'])
@jwt_required()
def update_machine(machine_id):
    try:
        machine = Machine.query.get_or_404(machine_id)
        data = request.get_json()

        machine.name = data.get('name', machine.name)
        machine.status = data.get('status', machine.status)
        machine.efficiency = data.get('efficiency', machine.efficiency)
        machine.temperature = data.get('temperature', machine.temperature)
        machine.vibration = data.get('vibration', machine.vibration)
        machine.last_maintenance = data.get('last_maintenance', machine.last_maintenance)

        db.session.commit()
        return jsonify(machine.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@machines_bp.route('/<machine_id>', methods=['DELETE'])
@jwt_required()
def delete_machine(machine_id):
    try:
        machine = Machine.query.get_or_404(machine_id)
        db.session.delete(machine)
        db.session.commit()
        return jsonify({'message': 'Machine deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@machines_bp.route('/generate-sample', methods=['POST'])
@jwt_required()
def generate_sample_machines():
    try:
        # Generate sample machines for testing
        sample_machines = [
            {
                'id': 'MACHINE-001',
                'name': 'Production Line A',
                'status': 'operational',
                'efficiency': random.randint(85, 100),
                'temperature': random.randint(20, 35),
                'vibration': round(random.uniform(0.1, 1.0), 1),
                'last_maintenance': '2024-01-15'
            },
            {
                'id': 'MACHINE-002',
                'name': 'Assembly Unit B',
                'status': 'warning',
                'efficiency': random.randint(70, 85),
                'temperature': random.randint(25, 40),
                'vibration': round(random.uniform(0.5, 1.5), 1),
                'last_maintenance': '2024-01-10'
            },
            {
                'id': 'MACHINE-003',
                'name': 'Quality Control C',
                'status': 'operational',
                'efficiency': random.randint(90, 100),
                'temperature': random.randint(18, 28),
                'vibration': round(random.uniform(0.1, 0.8), 1),
                'last_maintenance': '2024-01-20'
            },
            {
                'id': 'MACHINE-004',
                'name': 'Packaging Unit D',
                'status': 'maintenance',
                'efficiency': random.randint(60, 75),
                'temperature': random.randint(30, 45),
                'vibration': round(random.uniform(1.0, 2.0), 1),
                'last_maintenance': '2024-01-05'
            }
        ]

        created_machines = []
        for machine_data in sample_machines:
            # Check if machine already exists
            if not Machine.query.get(machine_data['id']):
                machine = Machine(
                    id=machine_data['id'],
                    name=machine_data['name'],
                    status=machine_data['status'],
                    efficiency=machine_data['efficiency'],
                    temperature=machine_data['temperature'],
                    vibration=machine_data['vibration'],
                    last_maintenance=machine_data['last_maintenance']
                )
                db.session.add(machine)
                created_machines.append(machine_data['id'])

        db.session.commit()
        return jsonify({
            'message': f'Created {len(created_machines)} sample machines',
            'machines': created_machines
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

