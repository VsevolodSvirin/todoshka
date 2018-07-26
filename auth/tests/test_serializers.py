from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from auth.authentication import get_token_pair
from auth.serializers import LoginSerializer, RegisterSerializer, RefreshSerializer

User = get_user_model()


class RegisterSerializerTestCase(TestCase):
    def test_user_creation(self):
        old_count = User.objects.count()

        user_attrs = {
            'username': 'Cool Guy',
            'email': 'cool_guy@smedialink.com',
            'password': '123'
        }

        user_serialized = RegisterSerializer(data=user_attrs)

        user_serialized.is_valid(raise_exception=True)
        user = user_serialized.save()

        new_count = User.objects.count()

        self.assertEqual(old_count + 1, new_count)

        user.delete()

    def test_required_fields(self):
        user_with_no_username = {
            'email': 'bad_guy@smedialink.com',
            'password': '123'
        }
        user_serialized = RegisterSerializer(data=user_with_no_username)
        with self.assertRaises(ValidationError):
            user_serialized.is_valid(raise_exception=True)

        user_with_no_email = {
            'username': 'Bad Guy',
            'password': '123'
        }
        user_serialized = RegisterSerializer(data=user_with_no_email)
        with self.assertRaises(ValidationError):
            user_serialized.is_valid(raise_exception=True)

        user_with_no_password = {
            'username': 'Bad Guy',
            'email': 'bad_guy@smedialink.com'
        }
        user_serialized = RegisterSerializer(data=user_with_no_password)
        with self.assertRaises(ValidationError):
            user_serialized.is_valid(raise_exception=True)


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        self.user_attrs = {
            'username': 'Cool Guy',
            'password': '123'
        }

        self.user_serialized = LoginSerializer(data=self.user_attrs)
        self.user_serialized.is_valid(raise_exception=True)

    def test_contains_expected_fields_without_token(self):
        data = self.user_serialized.data

        self.assertEqual(set(data.keys()), {'username', 'password'})

    def test_fields_content(self):
        data = self.user_serialized.data

        self.assertEqual(data['username'], self.user_attrs['username'])
        self.assertEqual(data['password'], self.user_attrs['password'])

    def test_required_fields(self):
        user_with_no_username = {'password': '123'}
        user_serialized = LoginSerializer(data=user_with_no_username)
        with self.assertRaises(ValidationError):
            user_serialized.is_valid(raise_exception=True)

        user_with_no_password = {'username': 'Bad Guy'}
        user_serialized = LoginSerializer(data=user_with_no_password)
        with self.assertRaises(ValidationError):
            user_serialized.is_valid(raise_exception=True)

    def test_validation(self):
        self.assertEqual(self.user_serialized.validate(data=self.user_serialized.data),
                         self.user_serialized.data)


class RefreshTokenSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Cool Guy',
                                             email='cool_guy@smedialink.com',
                                             password='123')
        self.tokens = get_token_pair(self.user)
        self.tokens_serialized = RefreshSerializer(data=self.tokens)
        self.tokens_serialized.is_valid(raise_exception=True)

    def tearDown(self):
        self.user.delete()

    def test_contains_expected_fields_without_token(self):
        data = self.tokens_serialized.data

        self.assertEqual(set(data.keys()), {'access_token', 'refresh_token'})

    def test_fields_content(self):
        data = self.tokens_serialized.data

        self.assertEqual(data['access_token'], self.tokens['access_token'])
        self.assertEqual(data['refresh_token'], self.tokens['refresh_token'])

    def test_required_fields(self):
        refresh_token_missing = self.tokens['access_token']
        tokens_serialized = RefreshSerializer(data=refresh_token_missing)
        with self.assertRaises(ValidationError):
            tokens_serialized.is_valid(raise_exception=True)

        access_token_missing = self.tokens['refresh_token']
        tokens_serialized = RefreshSerializer(data=access_token_missing)
        with self.assertRaises(ValidationError):
            tokens_serialized.is_valid(raise_exception=True)
