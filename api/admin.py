from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_time')
    search_fields = ('title', 'author__username')
    list_filter = ('type', 'created_time')