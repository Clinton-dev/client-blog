from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    default_about_message = "Just me, myself and I, exploring the universe of uknownment. I have a heart of love and a interest of lorem ipsum and mauris neque quam blog. I want to share my world with you."
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(null=True, default=default_about_message, max_length=250)

    def __str__(self):
        return f"{self.user.username} Profile"
