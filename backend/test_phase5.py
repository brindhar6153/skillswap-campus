import sys
import unittest
import json
from app import create_app, db
from app.models.user import User

class Phase5Test(unittest.TestCase):
    def setUp(self):
        # Create app using test configuration
        self.app = create_app()
        # Set testing mode and use a test SQLite db (or clean test PostgreSQL if preferred, but memory database is easiest)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration_and_login_flow(self):
        # 1. Test registration with valid fields
        payload = {
            "name": "Alice Smith",
            "email": "alice@university.edu",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
            "college": "State University",
            "course": "Computer Science"
        }
        response = self.client.post('/api/auth/register', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Registration successful. Please log in.")

        # Verify password is hashed in database
        with self.app.app_context():
            user = User.query.filter_by(email="alice@university.edu").first()
            self.assertIsNotNone(user)
            self.assertNotEqual(user.password_hash, "securepassword123")
            self.assertTrue(user.check_password("securepassword123"))

        # 2. Test duplicate email registration fails
        response = self.client.post('/api/auth/register', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Email already registered")

        # 3. Test validation errors: password mismatch
        payload_mismatch = payload.copy()
        payload_mismatch["email"] = "bob@university.edu"
        payload_mismatch["confirm_password"] = "mismatch"
        response = self.client.post('/api/auth/register', 
                                    data=json.dumps(payload_mismatch),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Passwords do not match.")

        # 4. Test validation errors: invalid email domain
        payload_invalid_domain = payload.copy()
        payload_invalid_domain["email"] = "alice@gmail.com"
        response = self.client.post('/api/auth/register', 
                                    data=json.dumps(payload_invalid_domain),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn("Only institutional email addresses", data['message'])

        # 5. Test login fails with invalid password
        login_payload = {
            "email": "alice@university.edu",
            "password": "wrongpassword"
        }
        response = self.client.post('/api/auth/login', 
                                    data=json.dumps(login_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Invalid email or password")

        # 6. Test login succeeds with correct password
        login_payload["password"] = "securepassword123"
        response = self.client.post('/api/auth/login', 
                                    data=json.dumps(login_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['name'], "Alice Smith")
        self.assertEqual(data['user']['college'], "State University")

        # 7. Test /api/auth/me endpoint (Authenticated)
        response = self.client.get('/api/auth/me')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['email'], "alice@university.edu")

        # 8. Test logout clears session
        response = self.client.post('/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        # 9. Verify /api/auth/me returns 401 Unauthorized after logout
        response = self.client.get('/api/auth/me')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Unauthorized access. Please login.")

if __name__ == '__main__':
    unittest.main()
