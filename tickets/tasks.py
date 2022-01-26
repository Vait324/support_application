from support_application.celery import app
from users.models import User

from .models import FromStaffNotification, FromUserNotification, Ticket


@app.task
def create_notification(user_id, ticket_id):
    '''Создание индикатора непрочитанных сообщений'''
    user = User.objects.get(pk=user_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    if user.is_staff and ticket.notif_from_staff.count() == 0:
        FromStaffNotification.objects.create(notificated_ticket=ticket)
    elif ticket.notif_from_user.count() == 0:
        FromUserNotification.objects.create(notificated_ticket=ticket)


@app.task
def delete_notification(user_id, ticket_id):
    '''Удаление индикатора непрочитанных сообщений'''
    user = User.objects.get(pk=user_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    if user.is_staff and ticket.notif_from_user.count() > 0:
        FromUserNotification.objects.get(notificated_ticket=ticket).delete()
    elif ticket.notif_from_staff.count() > 0:
        FromStaffNotification.objects.get(notificated_ticket=ticket).delete()
