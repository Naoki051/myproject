# apps/home/urls.py
from django.urls import path
from apps.home.views import IndexView, LoginView, SignUpView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]