from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api
from . import views

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/edit/', api.edit_profile, name='edit_profile'),
    path('profile/edit-password/', api.edit_password, name='edit_password'),
    path('friends/<uuid:id>/', api.friends, name='friends'),
    path('friends/<uuid:id>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<uuid:id>/<str:status>/', api.handle_friendship_request, name='handle_friendship_request'),
    path('activate-account/', views.activate_account, name='activate_account')
]


