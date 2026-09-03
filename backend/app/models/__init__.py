# Expose all database models for flask-migrate autodetect indexing
from app.models.user import User
from app.models.skill import Skill, UserSkill
from app.models.session import SwapRequest, Session
from app.models.transaction import CreditTransaction
from app.models.review import Review
from app.models.availability import UserAvailability
from app.models.utility import Notification, AuditLog

__all__ = [
    'User',
    'Skill',
    'UserSkill',
    'SwapRequest',
    'Session',
    'CreditTransaction',
    'Review',
    'UserAvailability',
    'Notification',
    'AuditLog'
]
