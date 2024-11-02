from django.urls import path
from . import views

urlpatterns = [
    path('', views.Profiles , name='profiles'),
    path('profile/<str:pk>',views.UserProfile, name = 'user-profile'),
    path('login/', views.loginUser ,name='login'),
    path('logout/', views.logoutUser, name= 'logout'),
    path('register/', views.registerUser, name= 'register')
]