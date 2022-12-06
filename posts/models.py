from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(null=True, max_length=250)
    description = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=timezone.now)
    image = models.ImageField(default="default-blog-banner.jpg", upload_to="blog_pics")
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.title} posts"


class Comment(models.Model):
    description = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return self.description[1:50]
