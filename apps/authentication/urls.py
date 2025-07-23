from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login_page/', login_page, name='login-page'),
    path('login/', user_login, name='user_login'),
    path('logout/', logout_page, name='logout-page'),
    path('register_page/', register_page, name='register-page'),
    path('register/', user_register, name='user-register'),

    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]
