"""Message model tests."""

# run these tests with:
# python3 -m unittest app.tests.test_message_model


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


class MessageModelTestCase(TestCase):
    """Tests creating a new message."""

    def setUp(self):
        """Create test client."""

        self.client = app.test_client()

    def add_user(self, name):
        """Add a user to the db for testing."""

        user = User(email=f"{name}@test.com", username=name, password="HASHED_PASSWORD")
        db.session.add(user)
        db.session.commit()
        return user

    def add_msg(self, message, id):
        """Add a message to the db for testing."""

        msg = Message(text=message, user_id=id)
        db.session.add(msg)
        db.session.commit()
        return msg

    def test_message_model(self):
        """Does basic model work?"""

        user = self.add_user("test")
        msg = self.add_msg("Test", user.id)
        self.assertEqual(msg.text, "Test")
        self.assertEqual(msg.user_id, user.id)

    def test_like_back_populate(self):
        """Does adding a User to a message's liked_by list back-populate to a User's likes?"""

        user = self.add_user("test")
        user2 = self.add_user("test2")
        msg = self.add_msg("Test", user.id)
        msg.liked_by.append(user2)
        db.session.commit()

        self.assertIn(msg, user2.likes)

    def test_liked_by_back_populate(self):
        """Does adding a message to a User's likes list back-populate to a Message's liked_by?"""

        user = self.add_user("test")
        user2 = self.add_user("test2")
        msg = self.add_msg("Test", user.id)
        user2.likes.append(msg)
        db.session.commit()

        self.assertIn(user2, msg.liked_by)

    def tearDown(self):
        """Clear testing data from User, Message, Follows tables."""

        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()
