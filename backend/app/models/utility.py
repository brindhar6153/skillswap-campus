from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    """Database model for tracking user alert notifications."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='notifications')

    def __repr__(self):
        return f"<Notification User:{self.user_id} Title:{self.title} Read:{self.is_read}>"


class AuditLog(db.Model):
    """Database model storing internal security action audit trails."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    action = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='audit_logs')

    def __repr__(self):
        return f"<AuditLog Action:{self.action} User:{self.user_id} Date:{self.created_at}>"
