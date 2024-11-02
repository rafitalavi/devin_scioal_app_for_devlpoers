from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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