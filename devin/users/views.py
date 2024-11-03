from django.shortcuts import render ,redirect
from .models import Profile ,Skill
from .utils import SearchProjects , paginationProfiles
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate ,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm , ProfileForm ,SkillForm
from django.contrib import messages
from django.db.models import Q #for search by multipl value

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
            return redirect('edit-account')
        else:
           messages.error(request,form.errors)
    context = {'page' : page ,'form':form}
    return render(request, 'users/login_register.html' ,context)



#profiles
def Profiles(request):
    profiles, search_query = SearchProjects(request)
    custom_range, profiles = paginationProfiles(request, profiles, 3)

    no_results = "No profiles found matching your search criteria." if not profiles else None

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'no_results': no_results
    }
    
    return render(request, 'users/profiles.html', context)

#user-profile
def UserProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = Skill.objects.filter(owner=profile).exclude(description__exact='')
    otherSkills = Skill.objects.filter(owner=profile, description='')
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

#user account
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile #one to one relationship
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context ={'profile': profile ,'skills': skills ,'projects':projects}
    return render(request, 'users/account.html',context)

#edit profile
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile #profile that login

    form  = ProfileForm(instance = profile)# prefill my info
    if request.method == 'POST':
        
      form  = ProfileForm(request.POST, request.FILES ,instance = profile) 
      if form.is_valid():
          form.save()  
          return redirect('profiles')
          
    context = {'form':form}
    return render(request, 'users/profile_form.html',context)

#add skill form create
@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile #profile that login
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request , 'Skill was created succesfully')
            return redirect('account')
  


    context = {'form':form}
    return render(request, 'users/skill_form.html',context)

#edit skill form
@login_required(login_url='login')
def UpdateSkill(request , pk):
    profile = request.user.profile #profile that login
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST , instance = skill)#sending particular data
        if form.is_valid():
            form.save()
            messages.success(request , 'Skill was updated succesfully')
           
            return redirect('account')
  


    context = {'form':form}
    return render(request, 'users/skill_form.html',context)
#delete

@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile #one to one rel with profile and project
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')# rediecting home page
         
        

    context = {'object': skill}
    return render(request,"delete_template.html",context)