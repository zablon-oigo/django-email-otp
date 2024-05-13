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
