"""Message View tests."""

# run these tests with:
# python3 -m unittest app.tests.test_message_views


from unittest import TestCase
from app import db, init_app
from app.models import Message, User
from app.user.user_util import CURR_USER_KEY

# Environment variables are handled in config.py and .env, no need to set here
app = init_app("config.TestConfig")

# Context is pushed so that it exists to create the tables
app.app_context().push()

# Create our tables, dropping first to ensure they are newly created
db.drop_all()
db.create_all()


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        self.testuser = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None,
        )

        db.session.commit()

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

    def test_add_message(self):
        """Can a user add a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_delete_message(self):
        """Can a user delete their message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            msg_to_delete = self.add_msg("sample text", self.testuser.id)

            resp = c.post(f"/messages/{msg_to_delete.id}/delete")
            self.assertEqual(resp.status_code, 302)

            msg_query = Message.query.one_or_none()
            self.assertIsNone(msg_query)

    def tearDown(self):
        """Clear testing data from User and Message tables."""

        User.query.delete()
        Message.query.delete()
        db.session.commit()
