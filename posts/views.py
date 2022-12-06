from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    DeleteView,
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin  # display flash message
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Comment, Tag
from .forms import CommentForm


def getPopularPosts():
    """returns list top five blog post based on comments"""
    popular = []
    posts = Post.objects.all()

    for post in posts:
        count = len(list(post.comment_set.all()))
        popular.append({"post": post, "comments": count})

    popular.sort(reverse=True, key=lambda item: item["comments"])
    return popular[0:5]


def index(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    posts = Post.objects.filter(Q(tags__name__icontains=q))
    paginated_posts = Paginator(posts, 2)
    popular = getPopularPosts()
    page_number = request.GET.get("page")
    page_obj = paginated_posts.get_page(page_number)
    tags = Tag.objects.all()
    context = {"posts": page_obj, "tags": tags, "popular": popular}
    return render(request, "posts/index.html", context)


class PostCreateView(SuccessMessageMixin, CreateView):
    model = Post
    fields = ["title", "description", "image", "tags"]
    success_url = reverse_lazy("home")
    success_message = "Blog post created successfully!"

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data.get("title")

            messages.success(
                request,
                f"{title} was created!",
            )
            return redirect("home")

        return render(request, self.template_name, {"form": form})


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["commentForm"] = CommentForm
        context[
            "comments"
        ] = self.object.comment_set.all()  # get all comments of the individual post
        return context


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ["title", "description", "image", "tags"]
    success_url = reverse_lazy("home")  # redirect to individual blog post page
    success_message = "Blog post updated successfully!"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("home")
    success_message = "Blog post deleted successfully!"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(author=self.request.user)


class CommentCreateView(SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(pk=kwargs["pk"])
            comment.save()
            return redirect("post-detail", kwargs["pk"])

        return render(request, self.template_name, {"form": form})


class CommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy("home")
    success_message = "Blog post deleted successfully!"
