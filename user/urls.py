from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('password_reset_email', views.password_reset_email, name='password_reset_email'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.set_new_password, name='set_new_password')
]