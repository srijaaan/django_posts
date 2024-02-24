from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        try:
            post.users_liked.get(id=user.id)
            return Response({'detail': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            post.likes += 1
            post.users_liked.add(user)
            post.save()
            return Response({'detail': 'Post liked'})

    @action(detail=True, methods=['post'])
    def unlike_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        try:
            post.users_liked.get(id=user.id)
            post.likes -= 1
            post.users_liked.remove(user)
            post.save()
            return Response({'detail': 'Post unliked'})
        except ObjectDoesNotExist:
            return Response({'detail': 'You have not liked this post yet'},)

    @action(detail=True, methods=['post'])
    def share_post(self, request, pk=None):
        post = self.get_object()
        post.shares += 1
        post.save()
        return Response({'detail': 'Post shared'})

    @action(detail=True, methods=['post'])
    def create_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def draft_post(self, request, pk=None):
        post = self.get_object()
        post.is_draft = True
        post.save()
        return Response({'detail': 'Post drafted'})

    @action(detail=True, methods=['post'])
    def schedule_post(self, request, pk=None):
        post = self.get_object()
        scheduled_time_str = request.data.get('scheduled_time')
        try:
            scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%d %H:%M:%S')
            post.scheduled_time = scheduled_time
            post.is_draft = False
            post.save()
            return Response({'detail': 'Post scheduled'})
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not (username and password and email):
            return Response({'error': 'Username, password, and email required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'detail': 'User created'})

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'detail': 'User deleted'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    @csrf_exempt
    def login_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'username':user.id,'token': token.key, 'createdby':user.username})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def logout_user(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({'detail': 'User logged out'})
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
