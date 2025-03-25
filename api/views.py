from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.models import User
from .models import Project, Contributor, Issue, Comment
from .permission import IsAuthor, IsProjectContributor
from .serializers import (ProjectSerializer, DetailedProjectSerializer, ContributorSerializer,
                          IssueSerializer, CommentSerializer)


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

    def check_permissions(self, request):
        super().check_permissions(request)

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