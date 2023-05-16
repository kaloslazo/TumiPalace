import unittest
from main import app, db, User

class MainTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the index page', response.data)

    def test_register(self):
        response = self.app.post('/register', data={
            'username': 'testuser',
            'userpass': 'testpassword',
            'submit': 'Register'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))

if __name__ == '__main__':
    unittest.main()
