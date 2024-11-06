from django.shortcuts import render ,redirect , get_object_or_404
from django.http import HttpResponse
from .models import Project , Tag
from django.contrib import messages
from .forms import ProjectForm ,reviewForm
from .utils import SearchProject ,paginationProjects
from django.db.models import Q #for search by multipl value
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
# def hello_world(request):
#     return render(request,"main.html")

def projects(request):
    # Get projects and search query
    projects, search_query = SearchProject(request)
    
    # Correct unpacking of pagination results
    custom_range, projects = paginationProjects(request, projects, 3)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }
    
    return render(request, 'projects/projects.html', context)



#single project
def project(request, pk):
    # Fetch the project object by ID, raising a 404 error if not found
    projectobj = Project.objects.get(id=pk)
    
    # Initialize an empty review form
    form = reviewForm()

    if request.method == 'POST':
        # Populate the form with POST data
        form = reviewForm(request.POST)
        if form.is_valid():  # Validate the form data
            # Create a review object but don't save it to the database yet
            review = form.save(commit=False)
            # Associate the review with the current project and user
            review.project = projectobj
            review.owner = request.user.profile
            # Save the review to the database
            review.save()
            # Redirect to the same project page to prevent duplicate submissions
            projectobj.getVoteCount
            messages.success(request, "Your comment is successfully submiitted")
            return redirect('project', pk=projectobj.id)

    # Render the project details and the review form on the template
    return render(request, 'projects/single-project.html', {
        'project': projectobj,
        'form': form  # Pass the form instance to handle any validation errors
    })

#create project
@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST': #request type
        # print(request.POST)
        form = ProjectForm(request.POST ,request.FILES)
        if form.is_valid(): #is valid or not
            project = form.save(commit=False) #creatting the object
            project.owner = profile #malike sathe join hocce
            project.save()
            return redirect('account')# rediecting home page
    context = {'form':form}
    return render(request,'projects/project_form.html',context)

#update
@login_required(login_url="login")#requred login
def updateproject(request ,pk):
    profile = request.user.profile #one to one rel with profile and project
    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance = project)
    if request.method == 'POST': #request type
        # print(request.POST)
        form = ProjectForm(request.POST ,request.FILES,instance = project)
        if form.is_valid(): #is valid or not
            form.save() #creatting the object
            return redirect('projects')# rediecting home page
    context = {'form':form}
    return render(request,'projects/project_form.html',context)
#delete
@login_required(login_url="login")
def deleteproject(request, pk):
    profile = request.user.profile #one to one rel with profile and project
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')# rediecting home page
         
        

    context = {'object': project}
    return render(request,"delete_template.html",context)


