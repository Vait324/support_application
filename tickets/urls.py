from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tickets.views import (MessageViewSet, StaffTicketsViewSet,
                           UserTicketsViewSet)

app_name = 'tickets'

router = DefaultRouter()

router.register('forstaff', StaffTicketsViewSet, basename='forstaff')
router.register('tickets', UserTicketsViewSet, basename='tickets')
router.register(r'tickets/(?P<ticket_id>\d+)/messages', MessageViewSet,
                basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
