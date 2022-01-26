from django.contrib import admin

from .models import (FromStaffNotification, FromUserNotification, Message,
                     Ticket)


class MessageInLine(admin.StackedInline):
    model = Message


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author',)
    list_filter = ('status',)
    search_fields = ('author',)
    inlines = (MessageInLine,)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'ticket')
    list_filter = ('author',)


@admin.register(FromUserNotification)
class FromUserNoti(admin.ModelAdmin):
    list_display = ('notificated_ticket',)


@admin.register(FromStaffNotification)
class FromStaffNoti(admin.ModelAdmin):
    list_display = ('notificated_ticket',)
