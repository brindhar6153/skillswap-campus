from datetime import datetime
from app.extensions import db

class User(db.Model):
    """User profile database model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=True)
    college = db.Column(db.String(100), nullable=True)
    grad_year = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Defaults to 2.00 credits per database specification design rules
    credit_balance = db.Column(db.Numeric(10, 2), default=2.00, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Level Constraint check to prevent negative balance values
    __table_args__ = (
        db.CheckConstraint('credit_balance >= 0', name='check_positive_credit_balance'),
        db.CheckConstraint('grad_year >= 2026', name='check_logical_grad_year'),
    )

    def set_password(self, password):
        """Hash and set the user password."""
        import bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Verify the password hash."""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


    # Relationships
    user_skills = db.relationship('UserSkill', back_populates='user', cascade='all, delete-orphan')
    availabilities = db.relationship('UserAvailability', back_populates='user', cascade='all, delete-orphan')
    credit_transactions = db.relationship('CreditTransaction', back_populates='user', cascade='all, delete-orphan', foreign_keys='CreditTransaction.user_id')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', back_populates='user', cascade='all, delete-orphan')

    # Note: Requests and Sessions have foreign keys mapping sender/recipient or teacher/learner
    # We will declare relationships in their respective model code definitions.

    def __repr__(self):
        return f"<User {self.email} ({self.full_name})>"
