from functools import wraps
from flask import session, jsonify, g
from app.models.user import User

def login_required(f):
    """Decorator ensuring endpoints can only be accessed by authenticated users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Authentication failed", "message": "Unauthorized access. Please login."}), 401
        
        from app.extensions import db
        user = db.session.get(User, user_id)
        if not user:
            session.clear()
            return jsonify({"error": "Authentication failed", "message": "Unauthorized access. Session invalid."}), 401
        
        # Bind the user to Flask's global namespace context
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function
