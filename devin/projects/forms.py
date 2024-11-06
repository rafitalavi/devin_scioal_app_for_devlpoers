from django.forms import ModelForm, widgets
from django import forms
from .models import Project ,Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project  # for which we want to create the form
         # fields ='__all__' #for all attribute we aslo can us list 
        fields = ['title', 'description', 'featured_image', 'tags', 'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})  # Set 'input' as a string
        #self.fileds['title'].widget.attrs.update({'class': 'input'}) single way to hnadle


#review form
class reviewForm(ModelForm):
    class Meta:
          model = Review
          fields = ['value', 'body']
          labels = {'value': 'place your vote',
                    'body':'Add a comment'}
    
    def __init__(self, *args, **kwargs):
        super(reviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})  # Set 'input' as a string
        #self.fileds['title'].widget.attrs.update({'class': 'input'}) single way to hnadle
       