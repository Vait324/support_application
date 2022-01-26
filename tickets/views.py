from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket
from .permissions import IsAuthorOrStaff, IsStaff
from .serializers import MessageSerializer, TicketSerializer
from .tasks import create_notification, delete_notification


class StaffMixin(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    pass


class UserTicketsApiView(APIView):
    '''Создание и просмотр собственных тикетов пользователя'''
    def get(self, request):
        user = request.user
        tickets = Ticket.objects.filter(author=user)
        serializer = TicketSerializer(tickets, many=True,)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, status='open')
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class MessageApiView(APIView):
    '''Обмен сообщениями между администрацией и авторами тикетов,
       автосоздание и удаление индикаторов'''
    permission_classes = (IsAuthorOrStaff,)

    def get(self, request, id=None):
        ticket = Ticket.objects.get(pk=id)
        self.check_object_permissions(request, ticket)
        messages = ticket.ticket_messages.all()
        serializer = MessageSerializer(messages, many=True)
        delete_notification.delay(request.user.id, id)
        return Response(serializer.data)

    def post(self, request, id=None):
        ticket = Ticket.objects.get(pk=id)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, ticket=ticket)
            create_notification.delay(request.user.id, id)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class StaffTicketsApiView(StaffMixin):
    '''Просмотр и изменение всех тикетов с фильтрацией по статусу,
    для админов'''
    permission_classes = (IsStaff,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)
