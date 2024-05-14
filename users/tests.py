from django.test import TestCase
from django.contrib.auth import get_user_model
User =get_user_model()

class UserManagerTest(TestCase):
    def test_create_user(self):
        user=User.objects.create_user(
            email="testuser@mail.com",
            password="secret"
        )
        self.assertEqual(user.email,"testuser@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()
        
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="secret")
    def test_create_superuser(self):
        admin_user=User.objects.create_superuser(
            email="superuser@mail.com",
            password="secret."
        )
        self.assertEqual(admin_user.email, "superuser@mail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@mail.com",
                password="secret.",
                is_superuser=False
            )
