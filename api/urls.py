from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, IssueViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('issues', IssueViewSet, basename='issues')
router.register('comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]