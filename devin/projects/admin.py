from django.contrib import admin
from .models import Project,Review,Tag


admin.site.register(Project) ## to show and register to admin panel
admin.site.register(Review) ## to show and register to admin panel
admin.site.register(Tag) ## to show and register to admin panel