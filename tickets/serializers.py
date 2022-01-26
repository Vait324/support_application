from rest_framework import serializers

from .models import Message, Ticket


class MessageSerializer(serializers.ModelSerializer):
    '''Сериализатор для сообщений'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('author', 'text')


class TicketSerializer(serializers.ModelSerializer):
    '''Сериализатор для тикетов'''
    author = serializers.StringRelatedField(read_only=True)
    ticket_messages = MessageSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(choices=Ticket.CHOICES, required=False)
    not_read = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'text', 'status', 'author',
                  'date', 'not_read', 'ticket_messages',)

    def get_not_read(self, obj):
        if self.context:
            notif = obj.notif_from_user.exists()
        else:
            notif = obj.notif_from_staff.exists()
        return notif
