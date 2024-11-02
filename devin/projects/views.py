from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm 
from django.contrib.auth.decorators import login_required
# def hello_world(request):
#     return render(request,"main.html")

def projects(request):
    projects = Project.objects.all() ## query for all projects in database
    context ={'projects': projects}
    return render(request, 'projects/projects.html' ,context )
def project(request,pk):
    projectobj = Project.objects.get(id=pk)
    # tags = projectobj.tags.all()

    print('projectoobj:',projectobj)
     # return render(request,'projects/single-project.html',{'project':projectobj ,'tags':tags} )
    return render(request,'projects/single-project.html',{'project':projectobj } )
@login_required(login_url="login")
def createproject(request):
    form = ProjectForm()
    if request.method == 'POST': #request type
        # print(request.POST)
        form = ProjectForm(request.POST ,request.FILES)
        if form.is_valid(): #is valid or not
            form.save() #creatting the object
            return redirect('projects')# rediecting home page
    context = {'form':form}
    return render(request,'projects/project_form.html',context)

#update
@login_required(login_url="login")#requred login
def updateproject(request ,pk):
    project = Project.objects.get(id=pk)

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
    project = Project.objects.get(id = pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')# rediecting home page
         
        

    context = {'object': project}
    return render(request,"projects/delete_template.html",context)
