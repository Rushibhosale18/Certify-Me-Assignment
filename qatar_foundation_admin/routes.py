from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Admin, Opportunity
import secrets

auth_bp = Blueprint('auth', __name__)
opp_bp = Blueprint('opportunities', __name__)

@auth_bp.route('/signup', methods=['POST'])
@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([full_name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
        
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
        
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({"error": "Email already registered"}), 400
        
    hashed_password = generate_password_hash(password, method='scrypt')
    new_admin = Admin(full_name=full_name, email=email, password_hash=hashed_password)
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Admin created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)
    
    admin = Admin.query.filter_by(email=email).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
        
    login_user(admin, remember=remember)
    if remember:
        session.permanent = True
    return jsonify({"status": "success", "message": "Logged in successfully", "email": email}), 200

@auth_bp.route('/logout', methods=['POST', 'GET'])
@auth_bp.route('/api/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out"}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
@auth_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
        
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        token = secrets.token_urlsafe(32)
        print(f"Password reset link for {email}: http://localhost:8000/reset/{token}")
        
    return jsonify({"status": "success", "message": "If the email exists, a reset link has been sent."}), 200

@opp_bp.route('/opportunities', methods=['GET'])
@opp_bp.route('/api/opportunities', methods=['GET'])
@login_required
def get_opportunities():
    user_ops = Opportunity.query.filter_by(admin_id=current_user.id).all()
    return jsonify({"status": "success", "data": [op.to_dict() for op in user_ops]}), 200

@opp_bp.route('/opportunities', methods=['POST'])
@opp_bp.route('/api/opportunities', methods=['POST'])
@login_required
def create_opportunity():
    data = request.get_json() or {}
    
    required_fields = ['name', 'duration', 'start_date', 'description', 'skills', 'category', 'future_opportunities']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400
            
    new_opp = Opportunity(
        name=data['name'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=data['skills'],
        category=data['category'],
        future_opportunities=data['future_opportunities'],
        max_applicants=data.get('max_applicants') or None,
        admin_id=current_user.id
    )
    
    db.session.add(new_opp)
    db.session.commit()
    
    return jsonify({"status": "success", "data": new_opp.to_dict()}), 201

@opp_bp.route('/opportunities/<int:id>', methods=['GET'])
@opp_bp.route('/api/opportunities/<int:id>', methods=['GET'])
@login_required
def get_opportunity(id):
    opp = Opportunity.query.get(id)
    if not opp or opp.admin_id != current_user.id:
        return jsonify({"error": "Opportunity not found"}), 404
        
    return jsonify({"status": "success", "data": opp.to_dict()}), 200

@opp_bp.route('/opportunities/<int:id>/edit', methods=['PUT', 'POST'])
@opp_bp.route('/api/opportunities/<int:id>/edit', methods=['PUT', 'POST'])
@login_required
def edit_opportunity(id):
    opp = Opportunity.query.get(id)
    if not opp or opp.admin_id != current_user.id:
        return jsonify({"error": "Opportunity not found"}), 404
        
    data = request.get_json() or {}
    opp.name = data.get('name', opp.name)
    opp.duration = data.get('duration', opp.duration)
    opp.start_date = data.get('start_date', opp.start_date)
    opp.description = data.get('description', opp.description)
    opp.skills = data.get('skills', opp.skills)
    opp.category = data.get('category', opp.category)
    opp.future_opportunities = data.get('future_opportunities', opp.future_opportunities)
    opp.max_applicants = data.get('max_applicants', opp.max_applicants)
    
    db.session.commit()
    return jsonify({"status": "success", "data": opp.to_dict()}), 200

@opp_bp.route('/opportunities/<int:id>', methods=['DELETE'])
@opp_bp.route('/api/opportunities/<int:id>', methods=['DELETE'])
@login_required
def delete_opportunity(id):
    opp = Opportunity.query.get(id)
    if not opp or opp.admin_id != current_user.id:
        return jsonify({"error": "Opportunity not found"}), 404
        
    db.session.delete(opp)
    db.session.commit()
    return jsonify({"status": "success"}), 200
