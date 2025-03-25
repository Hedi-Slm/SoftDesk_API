from rest_framework import permissions

from .models import Comment


class IsAuthor(permissions.BasePermission):
    """
    Permission to only allow authors of an object to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission to only allow contributors of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # If obj is Comment, we get his related project from Issue
        if isinstance(obj, Comment):
            project = obj.issue.project
        # If obj has project attribute then it's an Issue, so we get his related project
        elif hasattr(obj, 'project'):
            project = obj.project
        # Else it means that obj is Project, so we just get it
        else:
            project = obj

        return project.contributors.filter(user=request.user).exists()
