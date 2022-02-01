from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from tickets.models import Ticket
from tickets.permissions import IsAuthorOrStaff, IsStaff
from tickets.serializers import MessageSerializer, TicketSerializer
from tickets.tasks import create_notification, delete_notification


class StaffMixin(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    pass


class UserMixin(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    pass


class UserTicketsViewSet(UserMixin):
    '''Создание и просмотр собственных тикетов пользователя'''
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(author=user)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user,
                            status=Ticket.StatusChoices.OPEN)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MessageViewSet(UserMixin):
    '''Обмен сообщениями между администрацией и авторами тикетов,
       автосоздание и удаление индикаторов'''
    permission_classes = (IsAuthorOrStaff,)
    serializer_class = MessageSerializer

    def list(self, request, ticket_id):
        id = ticket_id
        ticket = Ticket.objects.get(pk=id)
        self.check_object_permissions(request, ticket)
        messages = ticket.ticket_messages.all()
        serializer = self.get_serializer(messages, many=True)
        delete_notification.delay(request.user.id, id)
        return Response(serializer.data)

    def create(self, request, ticket_id):
        id = ticket_id
        ticket = Ticket.objects.get(pk=id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, ticket=ticket)
            create_notification.delay(request.user.id, id)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class StaffTicketsViewSet(StaffMixin):
    '''Просмотр и изменение всех тикетов с фильтрацией по статусу,
    для админов'''
    permission_classes = (IsStaff,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)
