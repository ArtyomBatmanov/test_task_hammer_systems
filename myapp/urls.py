from django.urls import path
from .views import SendAuthCodeView, VerifyAuthCodeView, UserProfileView

urlpatterns = [
    path('auth/send-code/', SendAuthCodeView.as_view(), name='send-auth-code'),
    path('auth/verify-code/', VerifyAuthCodeView.as_view(), name='verify-auth-code'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
]
