"""Message View tests."""

# run these tests like:
#
# python3 -m unittest test_message_views.py


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

    def test_add_message(self):
        """Can a user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def tearDown(self):
        """Clear testing data from User and Message tables."""

        User.query.delete()
        Message.query.delete()
        db.session.commit()
