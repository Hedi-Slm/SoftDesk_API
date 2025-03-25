from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')


urlpatterns = [
    path('', include(router.urls)),
]