import re
from flask import Blueprint, request, jsonify, session, current_app, g
from app.extensions import db
from app.models.user import User
from app.utils.auth import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new student account (Phase 4 onboarding style)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Validation failed", "message": "Request body must be JSON"}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    # Required field verification
    if not name:
        return jsonify({"error": "Validation failed", "message": "Full name is required"}), 400
    if not email:
        return jsonify({"error": "Validation failed", "message": "Email address is required"}), 400
    if not password:
        return jsonify({"error": "Validation failed", "message": "Password is required"}), 400
    if not confirm_password:
        return jsonify({"error": "Validation failed", "message": "Password confirmation is required"}), 400

    # Email pattern syntax check
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Validation failed", "message": "Invalid email address format"}), 400

    # Configured College/Personal Email Domain check (supports '*' wildcard or comma-separated domains)
    allowed_domain = current_app.config.get('ALLOWED_EMAIL_DOMAIN', '*').strip()
    if allowed_domain and allowed_domain != '*' and '@' not in allowed_domain:
        domains = [d.strip().lower() for d in allowed_domain.split(',') if d.strip()]
        if '*' not in domains and not any(email.endswith(d) for d in domains):
            return jsonify({
                "error": "Validation failed", 
                "message": f"Only email addresses ending in {allowed_domain} are allowed."
            }), 400

    # Password validation
    if len(password) < 6:
        return jsonify({"error": "Validation failed", "message": "Password must be at least 6 characters long."}), 400

    if password != confirm_password:
        return jsonify({"error": "Validation failed", "message": "Passwords do not match."}), 400

    # Duplication check
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Conflict error", "message": "Email already registered"}), 409

    try:
        # Create and save user with default credit balance of 2.00
        new_user = User(
            full_name=name,
            email=email,
            credit_balance=2.00,
            is_verified=False # Registration is pending email verification / onboarding setup
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": "Registration successful. Please log in."
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": "Failed to complete registration."}), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login an existing student."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Validation failed", "message": "Request body must be JSON"}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "Validation failed", "message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    
    # Generic failure message to prevent email enumeration
    if not user or not user.check_password(password):
        return jsonify({"error": "Authentication failed", "message": "Invalid email or password"}), 401

    # Establish secure session cookie
    session.clear()
    session['user_id'] = user.id

    return jsonify({
        "success": True,
        "message": "Logged in successfully",
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "college": user.college,
            "course": user.major,
            "credits": float(user.credit_balance)
        }
    }), 200


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out the current student."""
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200


@auth_bp.route('/api/auth/me', methods=['GET'])
@login_required
def me():
    """Retrieve safe current user details."""
    user = g.current_user
    return jsonify({
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "college": user.college,
        "course": user.major,
        "major": user.major,
        "bio": user.bio,
        "grad_year": user.grad_year,
        "credits": float(user.credit_balance),
        "credit_balance": float(user.credit_balance)
    }), 200
