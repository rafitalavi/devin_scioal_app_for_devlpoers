from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta :
        model = Project #for which we want to create form 
        # fields ='__all__' #for all attribute we aslo can us list 
        fields = ['title','description','tags','demo_link', 'source_link']