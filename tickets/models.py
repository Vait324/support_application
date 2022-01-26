from django.db import models

from users.models import User


class Ticket(models.Model):
    '''Тикет пользователя'''
    CHOICES = (
        ('open', 'open'),
        ('closed', 'closed'),
        ('frozen', 'frozen')
    )
    title = models.CharField(
        max_length=50,
        help_text='Заголовок'
    )
    text = models.TextField(
        max_length=500,
        help_text='Опишите проблему',
    )
    status = models.CharField(
        max_length=30,
        choices=CHOICES,
        default='open'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    def __str__(self):
        return self.title


class Message(models.Model):
    '''Сообщения пользователей и администрации для тикетов'''
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )


class FromStaffNotification(models.Model):
    '''Индикатор непрочитанных сообщений для пользователей от админов'''
    notificated_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='notif_from_staff'
    )


class FromUserNotification(models.Model):
    '''Индикатор непрочитанных сообщений для админов от пользователей '''
    notificated_ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='notif_from_user'
    )
