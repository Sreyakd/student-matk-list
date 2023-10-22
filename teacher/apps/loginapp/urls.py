from django.urls import path
from apps.loginapp import views
urlpatterns = [
    path('user_login',views.LoginView.as_view())
]