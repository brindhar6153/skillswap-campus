from app.extensions import db

class UserAvailability(db.Model):
    """Database model storing student weekly availability schedule templates."""
    __tablename__ = 'user_availabilities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # 0 = Sunday, 6 = Saturday
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.CheckConstraint('day_of_week >= 0 AND day_of_week <= 6', name='check_valid_day_of_week'),
        db.CheckConstraint('start_time < end_time', name='check_start_before_end_time'),
    )

    # Relationships
    user = db.relationship('User', back_populates='availabilities')

    def __repr__(self):
        return f"<UserAvailability User:{self.user_id} Day:{self.day_of_week} {self.start_time}-{self.end_time}>"
