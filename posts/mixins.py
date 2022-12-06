from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class AuthorMixin(UserPassesTestMixin):
    login_url = "login"

    def test_func(self) -> bool:
        return self.request.user == "admin"

    def handle_no_permission(self):
        messages.warning(self.request, "Can't perform that action!")
        return redirect("home")
