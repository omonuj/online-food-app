import pytest
from django.urls import reverse
from accounts.models import User
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Onlinefood.settings')
django.setup()


@pytest.mark.django_db
def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post(reverse('registerUser'), {
        'first_name': 'Jonah',
        'last_name': 'Odoh',
        'username': 'jonahodoh',
        'email': 'jonah@example.com',
        'phone_number': '1234567890',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
    })

    assert response.status_code == 302  # Redirect after success
    assert User.objects.filter(username='jonahodoh').exists()


@pytest.mark.django_db
def test_register_user_duplicate_username(client, user_factory):
    """Test registration fails when username already exists."""
    user_factory(username='existinguser', email='unique@example.com')

    response = client.post(reverse('registerUser'), {
        'first_name': 'New',
        'last_name': 'User',
        'username': 'existinguser',
        'email': 'newemail@example.com',
        'phone_number': '1234567890',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
    })

    assert response.status_code == 200
    assert b"Username already exists" in response.content


@pytest.mark.django_db
def test_register_user_duplicate_email(client, user_factory):
    """Test registration fails when email already exists."""
    user_factory(username='uniqueuser', email='existing@example.com')

    response = client.post(reverse('registerUser'), {
        'first_name': 'New',
        'last_name': 'User',
        'username': 'newusername',
        'email': 'existing@example.com',
        'phone_number': '1234567890',
        'password': 'securepassword',
        'confirm_password': 'securepassword',
    })

    assert response.status_code == 200
    assert b"Email already exists" in response.content


@pytest.mark.django_db
def test_register_user_password_mismatch(client):
    """Test that registration fails when passwords don't match."""
    response = client.post(reverse('registerUser'), {
        'first_name': 'Jonah',
        'last_name': 'Odoh',
        'username': 'jonahodoh',
        'email': 'jonah@example.com',
        'phone_number': '1234567890',
        'password': 'securepassword',
        'confirm_password': 'wrongpassword',
    })

    assert response.status_code == 200
    assert b"Passwords do not match" in response.content
