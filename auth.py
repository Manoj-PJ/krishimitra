from flask import Blueprint, request, jsonify
from models.farmer import Farmer
from extensions import db
import re
from werkzeug.security import generate_password_hash

auth_routes = Blueprint('auth', __name__)

def validate_mobile(mobile):
    """Validate Indian mobile number format"""
    return re.match(r'^[6-9]\d{9}$', mobile) is not None

def validate_password(password):
    """Validate password requirements"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[^A-Za-z0-9]', password):
        return False
    return True

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'mobile', 'password', 'state', 'district']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "success": False,
                "message": f"{field.capitalize()} is required"
            }), 400

    # Validate mobile number format
    if not validate_mobile(data['mobile']):
        return jsonify({
            "success": False,
            "message": "Invalid Indian mobile number format (10 digits starting with 6-9)"
        }), 400

    # Validate password strength
    if not validate_password(data['password']):
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
        }), 400

    # Check if mobile already exists
    if Farmer.query.filter_by(mobile=data['mobile']).first():
        return jsonify({
            "success": False,
            "message": "Mobile number already registered"
        }), 409

    try:
        # Hash password before storing
        hashed_password = generate_password_hash(data['password'])
        
        new_farmer = Farmer(
            name=data['name'].strip(),
            mobile=data['mobile'],
            password=hashed_password,
            state=data['state'].strip(),
            district=data['district'].strip(),
            language=data.get('language', 'en'),
            crops=",".join(data.get('crops', []))  # Store crops as comma-separated string
        )

        db.session.add(new_farmer)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Farmer registered successfully",
            "farmer": {
                "id": new_farmer.id,
                "name": new_farmer.name,
                "mobile": new_farmer.mobile,
                "state": new_farmer.state,
                "district": new_farmer.district
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Registration failed",
            "error": str(e)
        }), 500

@auth_routes.route('/farmers', methods=['GET'])
def get_farmers():
    try:
        farmers = Farmer.query.all()
        return jsonify([{
            "id": farmer.id,
            "name": farmer.name,
            "mobile": farmer.mobile,
            "state": farmer.state,
            "district": farmer.district,
            "language": farmer.language,
            "crops": farmer.crops.split(',') if farmer.crops else []
        } for farmer in farmers])
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Failed to fetch farmers",
            "error": str(e)
        }), 500

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data or 'mobile' not in data or 'password' not in data:
        return jsonify({
            "success": False,
            "message": "Mobile and password are required"
        }), 400

    farmer = Farmer.query.filter_by(mobile=data['mobile']).first()
    
    if not farmer:
        return jsonify({
            "success": False,
            "message": "Invalid mobile number"
        }), 401

    # In a real implementation, use check_password_hash
    # For now, we'll just check if password matches
    if not farmer.check_password(data['password']):
        return jsonify({
            "success": False,
            "message": "Invalid password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "farmer": {
            "id": farmer.id,
            "name": farmer.name,
            "mobile": farmer.mobile,
            "state": farmer.state,
            "district": farmer.district,
            "language": farmer.language,
            "crops": farmer.crops.split(',') if farmer.crops else []
        }
    })