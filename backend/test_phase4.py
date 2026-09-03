import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.skill import Skill, UserSkill
from app.models.availability import UserAvailability

class Phase4AuthenticationOnboardingTest(unittest.TestCase):
    def setUp(self):
        # Set up test app context
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Seed some skills for onboarding tests
            self.skill_python = Skill(name="Python Programming", category="Technology")
            self.skill_spanish = Skill(name="Conversational Spanish", category="Languages")
            db.session.add(self.skill_python)
            db.session.add(self.skill_spanish)
            db.session.commit()

            # Retrieve seeded IDs
            self.skill_python_id = self.skill_python.id
            self.skill_spanish_id = self.skill_spanish.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # 1. Successful registration
    def test_01_successful_registration(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Registration successful. Please log in.")

        # Check DB entries and password hashing
        with self.app.app_context():
            user = User.query.filter_by(email="alice@college.edu").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.full_name, "Alice Smith")
            self.assertNotEqual(user.password_hash, "securepassword123")
            self.assertTrue(user.check_password("securepassword123"))

    # 2. Invalid email format
    def test_02_invalid_email(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice_invalid_email",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data['error'], "Validation failed")
        self.assertEqual(data['message'], "Invalid email address format")

    # 3. Disallowed email domain
    def test_03_disallowed_email_domain(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@gmail.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data['error'], "Validation failed")
        self.assertIn("Only institutional email addresses", data['message'])

    # 4. Duplicate email registration
    def test_04_duplicate_email(self):
        # Register Alice first
        payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=payload)

        # Attempt to register again
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 409)
        data = res.get_json()
        self.assertEqual(data['error'], "Conflict error")
        self.assertEqual(data['message'], "Email already registered")

    # 5. Password mismatch during registration
    def test_05_password_mismatch(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "differentpassword"
        }
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data['error'], "Validation failed")
        self.assertEqual(data['message'], "Passwords do not match.")

    # 6. Weak / invalid password length
    def test_06_weak_password(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "123",
            "confirm_password": "123"
        }
        res = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data['error'], "Validation failed")
        self.assertEqual(data['message'], "Password must be at least 6 characters long.")

    # 7. Successful login
    def test_07_successful_login(self):
        # Register first
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)

        # Login
        login_payload = {
            "email": "alice@college.edu",
            "password": "securepassword123"
        }
        res = self.client.post('/api/auth/login', json=login_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['email'], "alice@college.edu")

    # 8. Invalid login credentials
    def test_08_invalid_login(self):
        # Register Alice first
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)

        # Wrong password login
        login_payload = {
            "email": "alice@college.edu",
            "password": "wrongpassword"
        }
        res = self.client.post('/api/auth/login', json=login_payload)
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data['error'], "Authentication failed")
        self.assertEqual(data['message'], "Invalid email or password")

    # 9. Authenticated /api/auth/me
    def test_09_authenticated_me(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Get me info
        res = self.client.get('/api/auth/me')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['email'], "alice@college.edu")
        self.assertEqual(data['name'], "Alice Smith")

    # 10. Unauthenticated /api/auth/me
    def test_10_unauthenticated_me(self):
        res = self.client.get('/api/auth/me')
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data['error'], "Authentication failed")
        self.assertEqual(data['message'], "Unauthorized access. Please login.")

    # 11. Logout clears session
    def test_11_logout(self):
        # Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Logout
        res = self.client.post('/api/auth/logout')
        self.assertEqual(res.status_code, 200)

        # Attempt me route - should now be blocked
        res_me = self.client.get('/api/auth/me')
        self.assertEqual(res_me.status_code, 401)

    # 12. Protected onboarding route without authentication fails
    def test_12_protected_onboarding_route_unauthenticated(self):
        res = self.client.get('/api/onboarding/profile')
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data['error'], "Authentication failed")

    # 13. Create / update profile (Onboarding profile update)
    def test_13_create_update_profile(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Submit onboarding details
        profile_payload = {
            "college": "State College",
            "major": "Mechanical Engineering",
            "bio": "Avid learner and swimmer",
            "grad_year": 2028
        }
        res = self.client.post('/api/onboarding/profile', json=profile_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['college'], "State College")
        self.assertEqual(data['major'], "Mechanical Engineering")
        self.assertEqual(data['bio'], "Avid learner and swimmer")
        self.assertEqual(data['grad_year'], 2028)

        # Check updates are in database
        with self.app.app_context():
            user = User.query.filter_by(email="alice@college.edu").first()
            self.assertEqual(user.college, "State College")
            self.assertEqual(user.major, "Mechanical Engineering")

    # 14. Get skills catalog
    def test_14_get_skills(self):
        res = self.client.get('/api/skills')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(len(data) >= 2)
        # Should include python and spanish from setup
        names = [s['name'] for s in data]
        self.assertIn("Python Programming", names)
        self.assertIn("Conversational Spanish", names)

    # 15. Onboarding: Select teaching skills
    def test_15_select_teach_skills(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Select Python to teach
        skills_payload = {
            "teach": [{"skill_id": self.skill_python_id, "proficiency": "advanced"}],
            "learn": []
        }
        res = self.client.post('/api/onboarding/skills', json=skills_payload)
        self.assertEqual(res.status_code, 200)

        # Verify DB mappings
        with self.app.app_context():
            mappings = UserSkill.query.all()
            self.assertEqual(len(mappings), 1)
            teach_mapping = UserSkill.query.filter_by(role='teach').first()
            self.assertEqual(teach_mapping.skill_id, self.skill_python_id)
            self.assertEqual(teach_mapping.proficiency, "advanced")

    # 16. Onboarding: Select learning skills
    def test_16_select_learn_skills(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Select Spanish to learn
        skills_payload = {
            "teach": [],
            "learn": [{"skill_id": self.skill_spanish_id, "proficiency": "beginner"}]
        }
        res = self.client.post('/api/onboarding/skills', json=skills_payload)
        self.assertEqual(res.status_code, 200)

        # Verify DB mappings
        with self.app.app_context():
            mappings = UserSkill.query.all()
            self.assertEqual(len(mappings), 1)
            learn_mapping = UserSkill.query.filter_by(role='learn').first()
            self.assertEqual(learn_mapping.skill_id, self.skill_spanish_id)
            self.assertEqual(learn_mapping.proficiency, "beginner")

    # 17. Onboarding: Invalid skill ID rejection
    def test_17_invalid_skill_id(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Submit non-existent ID
        skills_payload = {
            "teach": [{"skill_id": 9999, "proficiency": "intermediate"}],
            "learn": []
        }
        res = self.client.post('/api/onboarding/skills', json=skills_payload)
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertEqual(data['error'], "Resource not found")
        self.assertIn("does not exist", data['message'])

    # 18. Create availability
    def test_18_create_availability(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Add slots
        avail_payload = [
            {"day_of_week": 1, "start_time": "09:00", "end_time": "11:00"},
            {"day_of_week": 3, "start_time": "14:00", "end_time": "16:00"}
        ]
        res = self.client.post('/api/onboarding/availability', json=avail_payload)
        self.assertEqual(res.status_code, 200)

        # Check DB
        with self.app.app_context():
            slots = UserAvailability.query.all()
            self.assertEqual(len(slots), 2)
            self.assertEqual(slots[0].day_of_week, 1)
            self.assertEqual(slots[0].start_time.strftime("%H:%M"), "09:00")
            self.assertEqual(slots[1].day_of_week, 3)

    # 19. Invalid availability where start time >= end time
    def test_19_invalid_availability_times(self):
        # Register and Login
        reg_payload = {
            "name": "Alice Smith",
            "email": "alice@college.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123"
        }
        self.client.post('/api/auth/register', json=reg_payload)
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "securepassword123"})

        # Start time later than end time
        avail_payload = [
            {"day_of_week": 1, "start_time": "14:00", "end_time": "10:00"}
        ]
        res = self.client.post('/api/onboarding/availability', json=avail_payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data['error'], "Validation failed")
        self.assertEqual(data['message'], "start_time must be strictly before end_time")

    # 20. User cannot modify another user's data
    def test_20_user_cannot_modify_another_users_data(self):
        # 1. Register User A and User B
        reg_a = {"name": "Alice A", "email": "alice@college.edu", "password": "password123", "confirm_password": "password123"}
        reg_b = {"name": "Bob B", "email": "bob@college.edu", "password": "password123", "confirm_password": "password123"}
        self.client.post('/api/auth/register', json=reg_a)
        self.client.post('/api/auth/register', json=reg_b)

        # 2. Login as User A
        self.client.post('/api/auth/login', json={"email": "alice@college.edu", "password": "password123"})

        # 3. Submit profile update for A
        profile_payload = {
            "college": "State College",
            "major": "Computer Science",
            "bio": "Alice's bio details",
            "grad_year": 2027
        }
        res = self.client.post('/api/onboarding/profile', json=profile_payload)
        self.assertEqual(res.status_code, 200)

        # 4. Verify in DB that User B's profile remains completely empty/unmodified
        with self.app.app_context():
            user_b = User.query.filter_by(email="bob@college.edu").first()
            self.assertIsNone(user_b.college)
            self.assertIsNone(user_b.major)
            self.assertIsNone(user_b.bio)

            # Check User A's profile did indeed update
            user_a = User.query.filter_by(email="alice@college.edu").first()
            self.assertEqual(user_a.college, "State College")
            self.assertEqual(user_a.major, "Computer Science")

if __name__ == '__main__':
    unittest.main()
