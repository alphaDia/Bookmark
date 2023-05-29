from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile


# Create your views here.
def user_login(request, *args, **kwargs):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd.get("username"), password=cd.get("password")
            )

            if not user:
                return HttpResponse("Invalid Login")

            if not user.is_active:
                return HttpResponse("Disabled Account")

            login(request, user)
            return HttpResponse("Authentication successfully")

    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def register(request, *args, **kwargs):
    if not request.method == "POST":
        user_form = UserRegistrationForm()
        return render(request, "account/register.html", {"user_form": user_form})

    user_form = UserRegistrationForm(request.POST)
    if not user_form.is_valid():
        return render(
            request,
            "account/register.html",
            {"user_form": user_form},
        )

    cd = user_form.cleaned_data
    new_user = user_form.save(commit=False)
    new_user.set_password(cd.get("password"))
    new_user.save()

    # Create a profile for the newly created user
    Profile.objects.create(user=new_user)

    # Welcome message
    messages.info(request, f"Welcome dear {new_user.username} to our platform")

    return render(
        request,
        "account/register_done.html",
        {"new_user": new_user},
    )


@login_required
def edit(request, *args, **kwargs):
    if not request.method == "POST":
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(
            request,
            "account/edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    user_form = UserEditForm(instance=request.user, data=request.POST)
    profile_form = ProfileEditForm(
        instance=request.user.profile, data=request.POST, files=request.FILES
    )

    if not user_form.is_valid() and not profile_form.is_valid():
        messages.error(request, _("Error updating your profile"))
        return render(
            request,
            "account/edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    user_form.save()
    profile_form.save()
    messages.success(request, _("Profile updated successfully"))

    return redirect("dashboard")


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


# class UserPasswordChangeView(PasswordChangeView):
#     form_class = UserPasswordChangeForm
