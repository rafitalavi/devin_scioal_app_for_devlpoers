from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

def paginationProjects(request, projects, results):
    # Set up pagination with specified results per page
    page = request.GET.get('page', 1)  # Default to page 1 if 'page' is not provided
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, show the first page
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # If page is out of range, show the last page
        page = paginator.num_pages
        projects = paginator.page(page)

    # Determine custom range for pagination controls
    left_index = max(1, int(page) - 1)
    right_index = min(int(page) + 2, paginator.num_pages + 1)
    custom_range = range(left_index, right_index)
    
    return custom_range, projects



    

def SearchProject(request):
    search_query = ''  # Default will be no value
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # Search tags based on the search_query
    tags = Tag.objects.filter(name__icontains=search_query)
    
    # Filter projects based on title, description, tags, or owner's name
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags) |  # Updated to use 'tags__in'
        Q(owner__name__icontains=search_query)
    )

    return projects, search_query
