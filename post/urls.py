from django.urls import path
from .views import (PostListApiView, PostCreateView, PostRetriewUpdateDestroyView, PostCommentListView,
                    PostCommentCreateView,CommentListCreateApiView,PostLikeListView, CommentRetriewView, CommentLikeListView , PostLikeApiView , CommentLikeApiView)

urlpatterns = [
    path('list/', PostListApiView.as_view(), name='posts_list'),
    path('create/', PostCreateView.as_view(),name='post_create'),
    path('<uuid:pk>/', PostRetriewUpdateDestroyView.as_view(),name='post_updated'),
    path('<uuid:pk>/likes/',PostLikeListView.as_view() , name="post_like"),
    path('<uuid:pk>/comments/',PostCommentListView.as_view() , name="post_comment"),
    path('<uuid:pk>/comments/create/',PostCommentCreateView.as_view() , name="post_comment_create"),
    path('comments/', CommentListCreateApiView.as_view() , name="comment_create"),
    path('comments/<uuid:pk>/', CommentRetriewView.as_view() , name="comment_detail"),
    path('comments/<uuid:pk>/likes/', CommentLikeListView.as_view() , name="comment_likes"),
    path('<uuid:pk>/edit/like/' , PostLikeApiView.as_view(), name='likes_edit'),
    path('<uuid:pk>/edit/comment/like/' , CommentLikeApiView.as_view(), name='comments_edit'),
]