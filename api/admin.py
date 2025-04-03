from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Project, Contributor, Issue, Comment


class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1
    autocomplete_fields = ['user']
    verbose_name = "Project Contributor"
    verbose_name_plural = "Project Contributors"


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0
    fields = ('title', 'priority', 'tag', 'status', 'assignee')
    autocomplete_fields = ['assignee']
    verbose_name = "Project Issue"
    verbose_name_plural = "Project Issues"
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('description', 'author', 'created_time')
    readonly_fields = ('created_time',)
    autocomplete_fields = ['author']
    verbose_name = "Issue Comment"
    verbose_name_plural = "Issue Comments"
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'contributor_count', 'issue_count', 'created_time')
    search_fields = ('title', 'description', 'author__username')
    list_filter = ('type', 'created_time')
    readonly_fields = ('created_time',)
    autocomplete_fields = ['author']
    inlines = [ContributorInline, IssueInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'type', 'author')
        }),
        ('Metadata', {
            'fields': ('created_time',),
            'classes': ('collapse',)
        }),
    )

    def contributor_count(self, obj):
        count = obj.contributors.count()
        url = reverse('admin:api_contributor_changelist') + f'?project__id__exact={obj.id}'
        return format_html('<a href="{}">{} contributors</a>', url, count)

    contributor_count.short_description = "Contributors"

    def issue_count(self, obj):
        count = obj.issues.count()
        url = reverse('admin:api_issue_changelist') + f'?project__id__exact={obj.id}'
        return format_html('<a href="{}">{} issues</a>', url, count)

    issue_count.short_description = "Issues"


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_link', 'created_time')
    search_fields = ('user__username', 'user__email', 'project__title')
    list_filter = ('created_time', 'project__type')
    readonly_fields = ('created_time',)
    autocomplete_fields = ['user', 'project']

    def project_link(self, obj):
        url = reverse('admin:api_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)

    project_link.short_description = "Project"


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'project_link', 'priority', 'tag', 'status', 'author', 'assignee', 'comment_count', 'created_time')
    search_fields = ('title', 'description', 'project__title', 'author__username', 'assignee__username')
    list_filter = ('priority', 'tag', 'status', 'created_time', 'project__type')
    readonly_fields = ('created_time',)
    autocomplete_fields = ['project', 'author', 'assignee']
    inlines = [CommentInline]
    list_editable = ('status', 'priority')

    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Project Information', {
            'fields': ('project', 'author')
        }),
        ('Issue Details', {
            'fields': ('priority', 'tag', 'status', 'assignee')
        }),
        ('Metadata', {
            'fields': ('created_time',),
            'classes': ('collapse',)
        }),
    )

    def project_link(self, obj):
        url = reverse('admin:api_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)

    project_link.short_description = "Project"

    def comment_count(self, obj):
        count = obj.comments.count()
        if count == 0:
            return '0 comments'
        url = reverse('admin:api_comment_changelist') + f'?issue__id__exact={obj.id}'
        return format_html('<a href="{}">{} comments</a>', url, count)

    comment_count.short_description = "Comments"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_preview', 'issue_link', 'project_name', 'author', 'created_time')
    search_fields = ('description', 'issue__title', 'author__username', 'issue__project__title')
    list_filter = ('created_time', 'issue__status', 'issue__project__type')
    readonly_fields = ('created_time',)
    autocomplete_fields = ['issue', 'author']

    fieldsets = (
        (None, {
            'fields': ('description',)
        }),
        ('Related Information', {
            'fields': ('issue', 'author')
        }),
        ('Metadata', {
            'fields': ('created_time',),
            'classes': ('collapse',)
        }),
    )

    def comment_preview(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description

    comment_preview.short_description = "Comment"

    def issue_link(self, obj):
        url = reverse('admin:api_issue_change', args=[obj.issue.id])
        return format_html('<a href="{}">{}</a>', url, obj.issue.title)

    issue_link.short_description = "Issue"

    def project_name(self, obj):
        url = reverse('admin:api_project_change', args=[obj.issue.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.issue.project.title)

    project_name.short_description = "Project"
