from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='user')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'project', 'created_time']
        read_only_fields = ['project', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']


class IssueSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='assignee',
                                                     required=False, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'project', 'author', 'assignee',
                  'assignee_id', 'comments', 'created_time']
        read_only_fields = ['author', 'project', 'created_time']


class DetailedProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    issues = IssueSerializer(many=True, read_only=True)

    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'issues', 'contributors', 'created_time']
        read_only_fields = ['author', 'created_time']

    def get_contributors(self, obj):
        contributors = Contributor.objects.filter(project=obj)
        return ContributorSerializer(contributors, many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'created_time']
        read_only_fields = ['created_time']