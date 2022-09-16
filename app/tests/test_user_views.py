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

    def test_invalid_signup(self):
        """Does User creation fail successfully if improper credentials are given?"""

        with self.client as c:
            resp = c.post(
                "/signup",
                data={
                    "username": "tester2",
                    "email": "invalid email",
                    "password": "password",
                },
            )

            # Make sure it refreshes the form page rather than redirect
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid email address.", resp.text)

    def test_duplicate_signup(self):
        """Does User creation fail successfully if duplicate credentials are given?"""

        with self.client as c:
            email_resp = c.post(
                "/signup",
                data={
                    "username": "tester2",
                    "email": "test@test.com",
                    "password": "password",
                },
            )
            self.assertEqual(email_resp.status_code, 200)
            self.assertIn("That email is already registered.", email_resp.text)

            username_resp = c.post(
                "/signup",
                data={
                    "username": "testuser",
                    "email": "newtest@test.com",
                    "password": "password",
                },
            )

            self.assertEqual(username_resp.status_code, 200)
            self.assertIn("That username is already taken.", username_resp.text)

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

            self.assertEqual(resp.status_code, 302)
            self.assertTrue(self.testuser.is_following(followed_by_user))

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

            self.assertEqual(resp.status_code, 302)
            self.assertTrue(self.testuser.is_followed_by(follower_of_user))

    def test_not_following(self):
        """Do the User-following functions work correctly when the users are not followers?"""

        follower_of_user = User(
            email="follower_of_test@test.com",
            username="follower_of_test",
            password="HASHED_PASSWORD",
        )
        not_follower = User(
            email="not_follower@test.com",
            username="not_follower",
            password="HASHED_PASSWORD",
        )

        db.session.add_all([follower_of_user, not_follower])
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = follower_of_user.id

            _ = c.post(f"/users/follow/{self.testuser.id}")

            self.assertTrue(self.testuser.is_followed_by(follower_of_user))
            self.assertFalse(self.testuser.is_followed_by(not_follower))
            self.assertFalse(self.testuser.is_following(not_follower))

    def tearDown(self):
        """Clear testing data from User, Message, Follows tables."""

        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()
