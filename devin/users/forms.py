from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Profile , Skill
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',  # Custom label for the 'first_name' field
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():  # Iterate over fields directly
            field.widget.attrs.update({'class': 'input'})  # Add 'input' class to each field

        #self.fileds['title'].widget.attrs.update({'class': 'input'}) single way to hnadle 

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username', 'location','bio','short_intro','profile_image','social_github','social_linkedin','social_twiiter','social_facebook','social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():  # Iterate over fields directly
            field.widget.attrs.update({'class': 'input'})  # Add 'input' class to each field

#add skill form
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():  # Iterate over fields directly
            field.widget.attrs.update({'class': 'input'})  # Add 'input' class to each field    
