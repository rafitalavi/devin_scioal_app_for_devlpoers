from django.shortcuts import render ,redirect
from .models import Profile ,Skill

from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate ,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages

#log in
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:#if user is loged in he can't see the log in page
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request,'Username or password is incorrect')#django 
            user = None
        
        user = authenticate(request, username=username, password=password)
        if user is not None:  # if user exists and password is correct
            login(request, user)  # login acceptance
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')#django 
    
    return render(request, 'users/login_register.html')

#logout
def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

#register/singup
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST': #request type
        # print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): #is valid or not
            user = form.save(commit=False) #creatting the object
            user.username = user.username.lower()  # Convert username to lowercase
            user.save()  # Save the user object
            messages.success(request , 'User Account is created')
            login(request, user)
            return redirect('profiles')
        else:
           messages.error(request,form.errors)
    context = {'page' : page ,'form':form}
    return render(request, 'users/login_register.html' ,context)



#profiles
def Profiles(request):
    profiles = Profile.objects.all()
    context = { 'profiles': profiles}
    return render(request, 'users/profiles.html',context)

#user-profile
def UserProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = Skill.objects.filter(owner=profile).exclude(description__exact='')
    otherSkills = Skill.objects.filter(owner=profile, description='')
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

