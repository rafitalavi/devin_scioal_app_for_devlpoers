from django.urls import path
from . import views

urlpatterns = [
    path('', views.Profiles , name='profiles'),
    path('profile/<str:pk>/',views.UserProfile, name = 'user-profile'),
    path('login/', views.loginUser ,name='login'),
    path('logout/', views.logoutUser, name= 'logout'),
    path('register/', views.registerUser, name= 'register'),
    path('account/', views.userAccount, name= 'account'),
    path('edit-account/', views.editAccount , name='edit-account'),
    path('create-skill',views.createSkill,name='create-skill'),
    path('update-skill/<str:pk>/', views.UpdateSkill,name='update-skill'),
    path('delete-skill/<str:pk>/',views.deleteSkill,name='delete-skill'),
    path('inbox', views.inbox , name='inbox'),
    path('message/<str:pk>/', views.veiwMessage , name='message'),
    path('create-message/<str:pk>/' , views.createMessage , name ='create-message'),

]