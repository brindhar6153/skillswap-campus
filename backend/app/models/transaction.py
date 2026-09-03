from datetime import datetime
from app.extensions import db

class CreditTransaction(db.Model):
    """Database ledger recording credit transactions for auditing purposes."""
    __tablename__ = 'credit_transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='SET NULL'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=True)
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.CheckConstraint("type IN ('initial_grant', 'hold_placement', 'hold_release', 'session_spend', 'session_earn', 'admin_adjustment')", name='check_valid_transaction_type'),
        db.CheckConstraint("type != 'admin_adjustment' OR admin_id IS NOT NULL", name='check_admin_id_during_adjustment'),
    )

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='credit_transactions')
    session = db.relationship('Session', back_populates='credit_transactions')
    admin = db.relationship('User', foreign_keys=[admin_id])

    def __repr__(self):
        return f"<CreditTransaction User:{self.user_id} Amount:{self.amount} Type:{self.type}>"
