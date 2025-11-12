from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from authentication.views import login, register, logout

app_name = 'authentication'

urlpatterns = [
    path('login/', csrf_exempt(login), name='login'),
    path('register/', csrf_exempt(register), name='register'),
    path('logout/', csrf_exempt(logout), name='logout'),
]