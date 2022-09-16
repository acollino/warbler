"""User model tests."""

# run these tests with:
# python3 -m unittest app.tests.test_user_model


from unittest import TestCase
from app import db, init_app
from app.models import Message, User, Follows

# Environment variables are handled in config.py and .env, no need to set here
app = init_app("config.TestConfig")

# Context is pushed so that it exists to create the tables
app.app_context().push()

# Create our tables, dropping first to ensure they are newly created
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test creating a new user account."""

    def setUp(self):
        """Create test client."""

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test2@test2.com", username="testuser2", password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_login_success(self):
        """Does User authentication work with correct login info?"""

        login = User.authenticate("testuser", "testuser")

        self.assertTrue(login)
        self.assertEqual(login, self.testuser)

    def test_login_rejection(self):
        """Does User authentication fail correctly with invalid login info?"""

        login = User.authenticate("testuser", "wrong password")

        self.assertFalse(login)

    def tearDown(self):
        """Clear testing data from User, Message, Follows tables."""

        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()
