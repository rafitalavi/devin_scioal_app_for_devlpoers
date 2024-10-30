from django.urls import path
from . import views
urlpatterns = [
    
    path('project/<str:pk>',views.project ,name= "project"),
    path('',views.projects ,name= "projects"),
    path('create-project/',views.createproject,name= "create-project"),
    path('update-project/<str:pk>',views.updateproject ,name='update-project'),
    path('delete-project/<str:pk>',views.deleteproject ,name='delete-project'),
]