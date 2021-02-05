from django.urls import path
from store.views import index, signup, login

urlpatterns = [
    path('', index, name='homepage'),
    path('signup', signup),
    path('login',login)
]
