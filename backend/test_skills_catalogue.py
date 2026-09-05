import unittest
import json
from app import create_app
from app.extensions import db
from app.models.skill import Skill, UserSkill
from app.models.user import User
from app.utils.skills_data import CATEGORIZED_SKILLS, SKILL_CATEGORIES

class TestSkillsConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    ALLOWED_EMAIL_DOMAIN = "*"
    APP_ENV = "testing"
    DEBUG = False

class SkillsCatalogueTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestSkillsConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_all_11_categories_present(self):
        """Verify all 11 categories exist in the seeded catalog."""
        skills = Skill.query.all()
        self.assertGreaterEqual(len(skills), 60)
        
        categories_in_db = {s.category for s in skills}
        for cat in SKILL_CATEGORIES:
            self.assertIn(cat, categories_in_db, f"Category '{cat}' missing from database")

    def test_all_required_skills_present(self):
        """Verify all specific technology skills requested by user are present."""
        required_skills = [
            "C", "C++", "Java", "Python", "JavaScript", "TypeScript", "Kotlin", "PHP",
            "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
            "Flask", "Django", "Spring Boot", "Android Development", "Jetpack Compose",
            "Flutter", "React Native", "MySQL", "PostgreSQL", "MongoDB", "SQLite",
            "Firebase", "SQL", "Git", "GitHub", "Docker", "Linux", "Data Structures",
            "Algorithms", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "OpenCV", "NLP", "Computer Vision", "Pandas", "NumPy", "Power BI",
            "Tableau", "Excel", "REST API", "GraphQL", "Generative AI",
            "AWS", "Azure", "Google Cloud", "Kubernetes", "CI/CD",
            "Cybersecurity", "Ethical Hacking", "Network Security",
            "Figma", "UI Design", "UX Design"
        ]
        
        skill_names_in_db = {s.name.lower() for s in Skill.query.all()}
        for req in required_skills:
            self.assertIn(req.lower(), skill_names_in_db, f"Required skill '{req}' missing from database")

    def test_no_duplicate_skills(self):
        """Verify there are no duplicate skill names."""
        skills = Skill.query.all()
        names = [s.name.lower() for s in skills]
        self.assertEqual(len(names), len(set(names)), "Duplicate skills detected in database")

    def test_get_skills_endpoint(self):
        """Test GET /api/skills returns all skills with category."""
        response = self.client.get('/api/skills')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 60)
        for item in data:
            self.assertIn('id', item)
            self.assertIn('name', item)
            self.assertIn('category', item)

    def test_get_skills_filtered_by_category(self):
        """Test GET /api/skills?category=... filters appropriately."""
        response = self.client.get('/api/skills?category=Mobile%20Development')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)
        for item in data:
            self.assertEqual(item['category'], 'Mobile Development')

    def test_get_skills_search(self):
        """Test GET /api/skills?search=... searches by skill name."""
        response = self.client.get('/api/skills?search=Python')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(any(s['name'] == 'Python' for s in data))

    def test_multi_skill_selection_and_matching(self):
        """Test multiple teaching and learning skill selection for users and matching compatibility."""
        # 1. Register Alice
        alice = User(full_name="Alice Dev", email="alice@test.com", credit_balance=2.00, is_verified=True)
        alice.set_password("Password123!")
        db.session.add(alice)

        # 2. Register Bob
        bob = User(full_name="Bob Learner", email="bob@test.com", credit_balance=2.00, is_verified=True)
        bob.set_password("Password123!")
        db.session.add(bob)
        db.session.commit()

        python_skill = Skill.query.filter_by(name="Python").first()
        react_skill = Skill.query.filter_by(name="React").first()
        kotlin_skill = Skill.query.filter_by(name="Kotlin").first()

        # Alice teaches Python and Kotlin, wants to learn React
        db.session.add(UserSkill(user_id=alice.id, skill_id=python_skill.id, role='teach', proficiency='advanced'))
        db.session.add(UserSkill(user_id=alice.id, skill_id=kotlin_skill.id, role='teach', proficiency='intermediate'))
        db.session.add(UserSkill(user_id=alice.id, skill_id=react_skill.id, role='learn', proficiency='beginner'))

        # Bob teaches React, wants to learn Python
        db.session.add(UserSkill(user_id=bob.id, skill_id=react_skill.id, role='teach', proficiency='advanced'))
        db.session.add(UserSkill(user_id=bob.id, skill_id=python_skill.id, role='learn', proficiency='beginner'))
        db.session.commit()

        # Login as Alice and test matches
        with self.client.session_transaction() as sess:
            sess['user_id'] = alice.id

        response = self.client.get('/api/matches')
        self.assertEqual(response.status_code, 200)
        matches = json.loads(response.data)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['user']['name'], "Bob Learner")
        self.assertTrue(matches[0]['reciprocal'])
        self.assertEqual(matches[0]['match_score'], 100)

if __name__ == '__main__':
    unittest.main()
