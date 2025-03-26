from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_time')
    search_fields = ('title', 'author__username')
    list_filter = ('type', 'created_time')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_time')
    search_fields = ('user__username', 'project__title')
    list_filter = ('created_time',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'author', 'assignee', 'created_time')
    search_fields = ('title', 'project__title', 'author__username', 'assignee__username')
    list_filter = ('priority', 'status', 'created_time')