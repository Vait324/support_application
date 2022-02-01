import pytest

from tickets.models import Message


@pytest.mark.django_db
def test_password(user1):
    user1.set_password('pass_word')
    assert user1.check_password('pass_word') is True


@pytest.mark.django_db
def test_ticket(user2_client, create_tickets):
    '''Пользователю доступны только собственные тикеты'''
    responce = user2_client.get('/tickets/')
    data = responce.json()
    assert len(data) == 2, ('Неверное отображение кол-ва тикетов')


@pytest.mark.django_db
def test_message_create(user2_client, create_tickets):
    '''Создание сообщения к тикету'''
    ticket = create_tickets[0]
    messages = Message.objects.count()
    data = {'author': user2_client, 'ticket': ticket, 'text': 'Message'}
    user2_client.post('/tickets/1/messages/', data=data)
    assert messages + 1 == Message.objects.count(), (
        'Ошибка при создании сообщения'
        )
