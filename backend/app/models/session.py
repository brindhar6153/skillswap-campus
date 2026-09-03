from datetime import datetime
from app.extensions import db

class SwapRequest(db.Model):
    """Database model tracking peer-to-peer exchange request invitations."""
    __tablename__ = 'swap_requests'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    teach_skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='SET NULL'), nullable=True)
    learn_skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='SET NULL'), nullable=True)
    
    status = db.Column(db.String(15), default='pending', nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.CheckConstraint('sender_id != receiver_id', name='check_sender_receiver_distinct'),
        db.CheckConstraint('teach_skill_id IS NOT NULL OR learn_skill_id IS NOT NULL', name='check_request_has_skills'),
        db.CheckConstraint("status IN ('pending', 'accepted', 'rejected', 'cancelled')", name='check_valid_request_status'),
    )

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    teach_skill = db.relationship('Skill', foreign_keys=[teach_skill_id])
    learn_skill = db.relationship('Skill', foreign_keys=[learn_skill_id])
    session = db.relationship('Session', back_populates='request', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<SwapRequest From:{self.sender_id} To:{self.receiver_id} Status:{self.status}>"


class Session(db.Model):
    """Scheduled swap session database representation details."""
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('swap_requests.id', ondelete='CASCADE'), nullable=False)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='RESTRICT'), nullable=False)
    
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_hours = db.Column(db.Numeric(4, 2), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    
    status = db.Column(db.String(15), default='scheduled', nullable=False)
    
    cancelled_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    cancelled_reason = db.Column(db.Text, nullable=True)
    
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.CheckConstraint('teacher_id != learner_id', name='check_teacher_learner_distinct'),
        db.CheckConstraint('duration_hours > 0', name='check_positive_duration'),
        db.CheckConstraint("status IN ('scheduled', 'completed', 'cancelled', 'disputed', 'expired')", name='check_valid_session_status'),
        db.CheckConstraint(
            "((status IN ('cancelled', 'expired') AND cancelled_by IS NOT NULL) OR (status NOT IN ('cancelled', 'expired') AND cancelled_by IS NULL))",
            name='check_audit_cancellation_fields'
        ),
    )

    # Relationships
    request = db.relationship('SwapRequest', back_populates='session')
    teacher = db.relationship('User', foreign_keys=[teacher_id])
    learner = db.relationship('User', foreign_keys=[learner_id])
    skill = db.relationship('Skill')
    cancellers = db.relationship('User', foreign_keys=[cancelled_by])
    
    credit_transactions = db.relationship('CreditTransaction', back_populates='session', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='session', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Session ID:{self.id} Teacher:{self.teacher_id} Learner:{self.learner_id} Status:{self.status}>"
