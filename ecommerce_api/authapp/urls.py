from django.urls import path
from .views import RegisterView, LoginView, ForgetPasswordView, ResetPasswordView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('forget_password',ForgetPasswordView.as_view()),
    path('reset_password',ResetPasswordView.as_view()),
]
