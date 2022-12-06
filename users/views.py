from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserRegistrationForm, UserUpdateForm


def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, "wrong details, try again!")
            return redirect("login")
    else:
        return render(request, "users/login.html")


def registration(request):
    context = {"title": "signup", "form": ""}

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            messages.success(
                request, f"{username} Account created successfully, you can now login!"
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
        context["form"] = form

    return render(request, "users/register.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, f"You were successfully, logged out!")
    return redirect("login")


@login_required
def settings(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)
