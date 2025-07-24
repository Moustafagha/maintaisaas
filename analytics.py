from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.machine import Machine
from src.models.activity import Activity
from src.models.predictive_data import PredictiveData
import random
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/predictive', methods=['GET'])
@jwt_required()
def get_predictive_analytics():
    try:
        # Get all machines and their predictive data
        machines = Machine.query.all()
        
        # Generate or get predictive data for each machine
        predictive_results = []
        for machine in machines:
            predictive_data = PredictiveData.query.filter_by(machine_id=machine.id).first()
            
            if not predictive_data:
                # Generate new predictive data
                predictive_data = PredictiveData(
                    machine_id=machine.id,
                    failure_probability=random.uniform(0.05, 0.35),
                    recommended_maintenance=random.randint(7, 45),
                    cost_savings=random.randint(1000, 15000)
                )
                db.session.add(predictive_data)
            
            predictive_results.append({
                'machine': machine.to_dict(),
                'predictive_data': predictive_data.to_dict()
            })
        
        db.session.commit()
        return jsonify(predictive_results), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    try:
        # Get basic statistics for dashboard
        total_machines = Machine.query.count()
        operational_machines = Machine.query.filter_by(status='operational').count()
        warning_machines = Machine.query.filter_by(status='warning').count()
        maintenance_machines = Machine.query.filter_by(status='maintenance').count()
        
        # Calculate average efficiency
        machines = Machine.query.all()
        avg_efficiency = sum(machine.efficiency for machine in machines) / len(machines) if machines else 0
        
        # Get recent activities count
        recent_activities = Activity.query.filter(
            Activity.timestamp >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Calculate total cost savings from predictive data
        total_cost_savings = db.session.query(db.func.sum(PredictiveData.cost_savings)).scalar() or 0

        stats = {
            'total_machines': total_machines,
            'operational_machines': operational_machines,
            'warning_machines': warning_machines,
            'maintenance_machines': maintenance_machines,
            'avg_efficiency': round(avg_efficiency, 1),
            'recent_activities': recent_activities,
            'total_cost_savings': round(total_cost_savings, 2)
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/maintenance-schedule', methods=['GET'])
@jwt_required()
def get_maintenance_schedule():
    try:
        machines = Machine.query.all()
        schedule = []
        
        for machine in machines:
            # Calculate urgency based on machine status and efficiency
            if machine.status == 'maintenance':
                urgency = 'high'
                recommended_days = random.randint(1, 7)
            elif machine.status == 'warning' or machine.efficiency < 80:
                urgency = 'medium'
                recommended_days = random.randint(7, 21)
            else:
                urgency = 'low'
                recommended_days = random.randint(21, 60)
            
            estimated_cost = random.randint(500, 5000)
            
            schedule.append({
                'machineId': machine.id,
                'machineName': machine.name,
                'urgency': urgency,
                'recommendedDays': recommended_days,
                'estimatedCost': estimated_cost,
                'currentStatus': machine.status
            })
        
        # Sort by urgency (high first)
        urgency_order = {'high': 0, 'medium': 1, 'low': 2}
        schedule.sort(key=lambda x: urgency_order[x['urgency']])
        
        return jsonify(schedule), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/cost-analysis', methods=['GET'])
@jwt_required()
def get_cost_analysis():
    try:
        # Get cost analysis data
        machines = Machine.query.all()
        total_maintenance_cost = 0
        total_savings = 0
        
        for machine in machines:
            # Simulate maintenance costs based on machine status
            if machine.status == 'maintenance':
                maintenance_cost = random.randint(2000, 8000)
            elif machine.status == 'warning':
                maintenance_cost = random.randint(1000, 4000)
            else:
                maintenance_cost = random.randint(200, 1000)
            
            total_maintenance_cost += maintenance_cost
            
            # Calculate potential savings from predictive maintenance
            potential_savings = maintenance_cost * random.uniform(0.2, 0.6)
            total_savings += potential_savings
        
        analysis = {
            'total_maintenance_cost': round(total_maintenance_cost, 2),
            'potential_savings': round(total_savings, 2),
            'cost_reduction_percentage': round((total_savings / total_maintenance_cost) * 100, 1) if total_maintenance_cost > 0 else 0,
            'monthly_savings': round(total_savings / 12, 2)
        }
        
        return jsonify(analysis), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/generate-sample-data', methods=['POST'])
@jwt_required()
def generate_sample_predictive_data():
    try:
        machines = Machine.query.all()
        created_data = []
        
        for machine in machines:
            # Check if predictive data already exists
            existing_data = PredictiveData.query.filter_by(machine_id=machine.id).first()
            if not existing_data:
                predictive_data = PredictiveData(
                    machine_id=machine.id,
                    failure_probability=random.uniform(0.05, 0.35),
                    recommended_maintenance=random.randint(7, 45),
                    cost_savings=random.randint(1000, 15000)
                )
                db.session.add(predictive_data)
                created_data.append(machine.id)
        
        db.session.commit()
        return jsonify({
            'message': f'Created predictive data for {len(created_data)} machines',
            'machines': created_data
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

