from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('register/',registerUser,name='register'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('book_service/',bookService,name='book_service'),
    path('home/',home,name='home'),
    path('profile/',userProfile,name='profile'),
    path('contact/',contact,name='contact'),
    path('in_process/',in_process,name='in_process'),
    path('delivered/',delivered,name='delivered'),
]
