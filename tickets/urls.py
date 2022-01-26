from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MessageApiView, StaffTicketsApiView, UserTicketsApiView

app_name = 'tickets'

router = DefaultRouter()

router.register('forstaff', StaffTicketsApiView, basename='forstaff')


urlpatterns = [
    path('', include(router.urls)),
    path('tickets/', UserTicketsApiView.as_view()),
    path('tickets/<int:id>/', MessageApiView.as_view())
]
