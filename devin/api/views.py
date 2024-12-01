from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project



@api_view(['GET'])
def getRoutes(request):
    routes = [
            {'GET':'api/projects'},
            {'GET':'api/projects/id'},
            {'POST':'api/projects/vote'},

            {'POST':'api/users/token'},
            {'POST':'api/users/token/refresh'},


   ]
    return Response(routes ) #safe we add more items than dictionary 


@api_view(['GET'])
# @permission_classes([IsAuthenticated]) #log in required to see all projects
def getProjects(request):
    print('USER:' ,request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects , many = True) #converting it into jsn format
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request , pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects , many = False) #converting it into jsn format if i want to show one item
    return Response(serializer.data)

# Voting
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = project.obj.get(id = pk)
    user = request.user
    data = request.data
    print('DATA:',data)
    serializer = ProjectSerializer(serializer.data , many= False)
    return Response(serializer.data)