from django.urls import path
from . import views
from .views import (
    CommentDeleteView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
    CommentCreateView,
)

urlpatterns = [
    path("", views.index, name="home"),
    path("posts/create/", PostCreateView.as_view(), name="create-post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "comment/<int:pk>/create/", CommentCreateView.as_view(), name="create-comment"
    ),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
]
