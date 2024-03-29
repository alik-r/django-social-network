from django.urls import path

from . import api 

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:id>/', api.post_detail, name='post_detail'),
    path('<uuid:id>/comment/', api.post_create_comment, name='post_create_comment'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('<uuid:id>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:id>/report/', api.post_report, name='post_report'),
    path('<uuid:id>/like/', api.post_like, name='post_like'),
    path('trends/', api.trend_list, name='trend_list'),
    path('trends/<uuid:id>/', api.trend_detail, name='trend_detail'),
]