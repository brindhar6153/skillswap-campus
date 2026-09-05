"""Production database initializer and seed script for SkillSwap Campus."""
import os
import sys
from app import create_app
from app.extensions import db
from app.models.skill import Skill

def init_production_db():
    print("Connecting to database and creating tables...")
    app = create_app()
    with app.app_context():
        db.create_all()
        print("All tables created successfully.")

from app.utils.skills_data import CATEGORIZED_SKILLS

def seed_skills():
    """Idempotently seed all categorized technology skills without duplicates or deleting existing data."""
    added_count = 0
    updated_count = 0
    for s_info in CATEGORIZED_SKILLS:
        name = s_info["name"].strip()
        category = s_info["category"].strip()
        
        # Check if skill already exists (case-insensitive)
        existing = Skill.query.filter(db.func.lower(Skill.name) == name.lower()).first()
        if not existing:
            db.session.add(Skill(name=name, category=category))
            added_count += 1
        else:
            # Update category if needed
            if existing.category != category:
                existing.category = category
                updated_count += 1
                
    if added_count > 0 or updated_count > 0:
        db.session.commit()
    print(f"Skills catalog synchronized: {added_count} added, {updated_count} categories updated. Total in catalog: {Skill.query.count()}.")

def init_production_db():
    print("Connecting to database and creating tables...")
    app = create_app()
    with app.app_context():
        db.create_all()
        print("All tables created successfully.")
        seed_skills()

if __name__ == "__main__":
    init_production_db()
