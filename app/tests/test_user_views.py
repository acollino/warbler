"""User views tests."""

# run these tests with:
# python3 -m unittest app.tests.test_user_model


from unittest import TestCase
from app import db, init_app
from app.models import Message, User, Follows
from app.user.user_util import CURR_USER_KEY

# Environment variables are handled in config.py and .env, no need to set here
app = init_app("config.TestConfig")

# Context is pushed so that it exists to create the tables
app.app_context().push()

# Create our tables, dropping first to ensure they are newly created
db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test creating a new user account."""

    def setUp(self):
        """Create test client."""

        self.client = app.test_client()
        self.testuser = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None,
        )
        db.session.commit()

    def test_follow_others(self):
        """Can a user follow another?"""

        followed_by_user = User(
            email="followed_by_test@test.com",
            username="followed_by_test",
            password="HASHED_PASSWORD",
        )

        db.session.add(followed_by_user)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post(f"/users/follow/{followed_by_user.id}")

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(self.testuser.is_following(followed_by_user), True)

    def test_followed_by_others(self):
        """Can a user be followed by another?"""

        follower_of_user = User(
            email="follower_of_test@test.com",
            username="follower_of_test",
            password="HASHED_PASSWORD",
        )

        db.session.add(follower_of_user)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = follower_of_user.id

            resp = c.post(f"/users/follow/{self.testuser.id}")

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(self.testuser.is_followed_by(follower_of_user), True)

    def tearDown(self):
        """Clear testing data from User, Message, Follows tables."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()
