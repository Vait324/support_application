import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tickets.models import Ticket
from users.models import User


@pytest.fixture
def user1(db):
    return User.objects.create_user('test_user')


@pytest.fixture
def user2(db):
    return User.objects.create_user('test_user2')


@pytest.fixture
def token(user2):
    refresh = RefreshToken.for_user(user2)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def user2_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client


@pytest.fixture
def create_tickets(user1, user2):
    tickets = Ticket.objects.bulk_create([
        Ticket(title='Title1', text='1text_text', author=user2),
        Ticket(title='Title2', text='2text_text', author=user2),
        Ticket(title='Title3', text='3text_text', author=user1)
    ])
    return tickets
