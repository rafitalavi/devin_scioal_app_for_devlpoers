from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import Project , Tag
from .forms import ProjectForm 
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
    custom_range, projects = paginationProjects(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }
    
    return render(request, 'projects/projects.html', context)



#single project
def project(request,pk):
    projectobj = Project.objects.get(id=pk)
    # tags = projectobj.tags.all()

    print('projectoobj:',projectobj)
     # return render(request,'projects/single-project.html',{'project':projectobj ,'tags':tags} )
    return render(request,'projects/single-project.html',{'project':projectobj } )


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
