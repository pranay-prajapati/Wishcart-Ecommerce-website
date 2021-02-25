from django.urls import path
from store.views import Index, Signup, Login, Logout, Cart, Checkout, OrderView

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', OrderView.as_view(), name='order'),
]
