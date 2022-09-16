"""User views tests."""

# run these tests with:
# python3 -m unittest app.tests.test_user_views


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

    def test_login_success(self):
        """Can an existing user successfully log in?"""

        with self.client as c:
            resp = c.post(
                "/login",
                data={
                    "username": "testuser",
                    "password": "testuser",
                },
                follow_redirects=True,
            )

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", resp.text)
            self.assertIn("Hello, testuser!", resp.text)

    def test_login_fail(self):
        """Does an invalid login successfully fail?"""
        with self.client as c:
            wrong_pw_resp = c.post(
                "/login",
                data={
                    "username": "testuser",
                    "password": "wrongpw",
                },
            )
            self.assertEqual(wrong_pw_resp.status_code, 200)
            self.assertIn("Invalid credentials.", wrong_pw_resp.text)

            empty_login_resp = c.post(
                "/login",
                data={
                    "username": "",
                    "password": "",
                },
            )
            self.assertEqual(empty_login_resp.status_code, 200)
            self.assertIn("This field is required", empty_login_resp.text)

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

    def test_view_profile(self):
        """Does the user profile page load correctly?"""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", resp.text)
            self.assertIn("Followers", resp.text)
            self.assertIn("Likes", resp.text)

    def test_edit_profile(self):
        """Can a user edit their profile page?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser.id
            resp = c.post(
                f"/users/profile",
                data={
                    "username": "newname",
                    "bio": "About this user",
                    "location": "Somewhere",
                    "password": "testuser",
                },
                follow_redirects=True,
            )

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@newname", resp.text)
            self.assertIn("About this user", resp.text)
            self.assertIn("Somewhere", resp.text)

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

    def test_toggle_like(self):
        """Can a user successfully like or unlike a post?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # likes list should be initially empty
            self.assertEqual(self.testuser.likes, [])

            # must add a new user and msg, since you cannot like your own message
            user_2 = self.add_user("second")
            msg = self.add_msg("Sample text", user_2.id)

            resp_like = c.post(f"/users/add_like/{msg.id}")
            self.assertEqual(resp_like.status_code, 302)
            self.assertEqual(self.testuser.likes, [msg])

            # after a post is liked, a repeat request should remove the like
            resp_unlike = c.post(f"/users/add_like/{msg.id}")
            self.assertEqual(resp_unlike.status_code, 302)
            self.assertEqual(self.testuser.likes, [])

    def test_delete(self):
        """Can a user successfully delete their account?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            intial_count = User.query.filter(User.id == self.testuser.id).count()

            resp = c.post(f"/users/delete")
            delete_count = User.query.filter(User.id == self.testuser.id).count()

            self.assertEqual(intial_count, 1)
            self.assertEqual(delete_count, 0)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/signup")

    def tearDown(self):
        """Clear testing data from User, Message, Follows tables."""

        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.commit()
