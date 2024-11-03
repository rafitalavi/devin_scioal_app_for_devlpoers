
from django.db.models import Q #for search by multipl value
from .models import Profile ,Skill
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def paginationProfiles(request, profiles, results):
    # Set up pagination with the specified results per page
    page = request.GET.get('page', 1)  # Default to page 1 if 'page' is not provided
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, show the first page
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # If page is out of range, show the last page
        page = paginator.num_pages
        profiles = paginator.page(page)

    # Calculate custom range for pagination controls
    current_page = int(page)
    left_index = max(1, current_page - 1)
    right_index = min(current_page + 2, paginator.num_pages + 1)
    custom_range = range(left_index, right_index)

    return custom_range, profiles

def SearchProjects(request):
    search_query = '' #default will be no value
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains=search_query)#search by skill it is child element    
    print('SEARCH:',search_query)    
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                    Q( short_intro__icontains = search_query) |
                                    Q(skill__in=skills)
                                    )#lower case conversion default will  show all profiles by name or shot_intro
    return profiles,search_query