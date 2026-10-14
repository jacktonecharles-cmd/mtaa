from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import RegisterForm, ProfileForm


class MtaaBizLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to MtaaBiz Kenya, {user.username}!")
            return redirect("core:home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You've been logged out.")
    return redirect("core:home")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})
