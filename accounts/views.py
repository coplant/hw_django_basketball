from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render

from accounts.forms import CustomUserCreationForm, CustomUserLoginForm, UserProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == "POST":
            form = CustomUserLoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
            return render(request, "accounts/login.html", {"form": form})
        else:
            form = CustomUserLoginForm()
            return render(request, "accounts/login.html", {"form": form})


def is_staff(user):
    return user.is_authenticated and user.is_staff


def register_view(request):
    if not is_staff(request.user):
        return redirect(settings.LOGIN_URL)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def me_view(request):
    if not request.user:
        return redirect(settings.LOGIN_URL)

    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if "change_photo" in request.POST:
            if form.is_valid():
                form.save()
                return redirect("me")

        elif "delete_photo" in request.POST:
            if user.profile_image:
                user.profile_image.delete()
                return redirect("me")

    else:
        form = UserProfileForm(instance=user)
    return render(request, "accounts/me.html", {"user": request.user, "form": form})
