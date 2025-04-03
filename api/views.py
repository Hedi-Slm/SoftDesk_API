from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.models import User
from .models import Project, Contributor, Issue, Comment
from .permission import IsAuthor, IsProjectContributor
from .serializers import (ProjectSerializer, DetailedProjectSerializer, ContributorSerializer,
                          DetailedIssueSerializer, IssueSerializer, CommentSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthor]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedProjectSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # Set the current user as author and contributor
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        contributor = Contributor.objects.create(user=user, project=project)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_contributor(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'User ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        contributor = get_object_or_404(Contributor, user__id=user_id, project=project)

        # Don't allow removing the project author
        if project.author == contributor.user:
            return Response(
                {'error': 'Cannot remove the project author'},
                status=status.HTTP_400_BAD_REQUEST
            )

        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'assignee', 'author']
    ordering_fields = ['priority', 'status', 'tag']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedIssueSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Issue.objects.all().order_by('-created_time')

    def get_serializer_context(self):
        """ Add project to serializer context,so it can be used in validation """
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            project_id = self.request.data.get('project')
            if project_id:
                try:
                    context['project'] = Project.objects.get(id=project_id)
                except (Project.DoesNotExist, ValueError):
                    pass
        return context

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['issue']
    ordering_fields = ['created_time', 'issue']

    def get_queryset(self):
        # Only allow comments for issues in projects the user is a contributor of the project
        return Comment.objects.filter(issue__project__contributors__user=self.request.user).order_by('-created_time')

    def perform_create(self, serializer):
        issue_id = self.request.data.get('issue')
        issue = get_object_or_404(Issue, id=issue_id)

        serializer.save(author=self.request.user, issue=issue)
