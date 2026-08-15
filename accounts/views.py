from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm
)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            # التعديل هنا: أضفنا الـ backend لمنع التضارب مع allauth
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required
def profile(request):
    return render(
        request,
        'accounts/profile.html',
        {'profile': request.user.profile}
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('profile')

    else:
        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(
        request,
        'accounts/edit_profile.html',
        context
    )