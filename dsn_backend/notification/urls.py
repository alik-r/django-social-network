from django.urls import path

from . import api

urlpatterns = [
    path('', api.notification_list, name='notification_list'),
    path('<uuid:id>/read/', api.read_notification, name='read_notification')
]
