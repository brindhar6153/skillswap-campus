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

        # Seed initial skills if table is empty
        if Skill.query.count() == 0:
            initial_skills = [
                {"name": "Python Programming", "category": "Computer Science"},
                {"name": "Data Structures & Algorithms", "category": "Computer Science"},
                {"name": "Web Development (React)", "category": "Web & Mobile"},
                {"name": "Calculus II", "category": "Mathematics"},
                {"name": "Linear Algebra", "category": "Mathematics"},
                {"name": "Organic Chemistry", "category": "Chemistry"},
                {"name": "Spanish Language", "category": "Languages"},
                {"name": "French Language", "category": "Languages"},
                {"name": "Graphic Design & UI/UX", "category": "Design"},
                {"name": "Public Speaking & Debate", "category": "Communication"},
                {"name": "Academic Writing", "category": "Humanities"},
                {"name": "Microeconomics", "category": "Business & Economics"},
            ]
            for s in initial_skills:
                db.session.add(Skill(name=s["name"], category=s["category"]))
            db.session.commit()
            print(f"Seeded {len(initial_skills)} foundational academic skills.")
        else:
            print(f"Database already contains {Skill.query.count()} skills. Skipping seeding.")

if __name__ == "__main__":
    init_production_db()
