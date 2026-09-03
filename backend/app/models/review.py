from datetime import datetime
from app.extensions import db

class Review(db.Model):
    """Database model for post-session double-blind reviews."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    is_visible = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.UniqueConstraint('session_id', 'reviewer_id', name='uq_session_reviewer'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_valid_rating_range'),
        db.CheckConstraint('reviewer_id != reviewee_id', name='check_reviewer_reviewee_distinct'),
    )

    # Relationships
    session = db.relationship('Session', back_populates='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
    reviewee = db.relationship('User', foreign_keys=[reviewee_id])

    def __repr__(self):
        return f"<Review Session:{self.session_id} Reviewer:{self.reviewer_id} Rating:{self.rating}>"
