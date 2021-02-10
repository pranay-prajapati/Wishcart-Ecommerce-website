from django.urls import path
from store.views import Index, Signup, Login

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view()),
    path('login', Login.as_view())
]
