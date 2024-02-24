# myproject/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import PostViewSet, UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like_post'}), name='post-like'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike_post'}), name='post-unlike'),
    path('posts/<int:pk>/share/', PostViewSet.as_view({'post': 'share_post'}), name='post-share'),
    path('posts/<int:pk>/comment/', PostViewSet.as_view({'post': 'create_comment'}), name='post-comment'),
    path('posts/<int:pk>/draft/', PostViewSet.as_view({'post': 'draft_post'}), name='post-draft'),
    path('posts/<int:pk>/schedule/', PostViewSet.as_view({'post': 'schedule_post'}), name='post-schedule'),
    path('login/', UserViewSet.as_view({'post': 'login_user'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout_user'}), name='logout'),
]
