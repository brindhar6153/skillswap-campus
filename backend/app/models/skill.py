from datetime import datetime
from app.extensions import db

class Skill(db.Model):
    """Global lookup catalog database model for tradeable skills."""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user_mappings = db.relationship('UserSkill', back_populates='skill', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Skill {self.name} - {self.category}>"


class UserSkill(db.Model):
    """Join table mapping students to their teachable/learning skills portfolios."""
    __tablename__ = 'user_skills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    
    # Must be 'teach' or 'learn'
    role = db.Column(db.String(10), nullable=False)
    proficiency = db.Column(db.String(15), default='beginner', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Database Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'skill_id', 'role', name='uq_user_skill_role'),
        db.CheckConstraint("role IN ('teach', 'learn')", name='check_valid_skill_role'),
        db.CheckConstraint("proficiency IN ('beginner', 'intermediate', 'advanced')", name='check_valid_proficiency'),
    )

    # Relationships
    user = db.relationship('User', back_populates='user_skills')
    skill = db.relationship('Skill', back_populates='user_mappings')

    def __repr__(self):
        return f"<UserSkill User:{self.user_id} Skill:{self.skill_id} Role:{self.role}>"
