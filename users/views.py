from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm,UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView)

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    pass


class UserPasswordResetView(PasswordResetView):
    form = PasswordResetForm()
    form_class = PasswordResetForm
    template_name = 'users/resetpassword.html'
    extra_context = {'form': form}
    subject_template_name = 'users/password_reset_subject.txt'
    html_email_template_name = 'users/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm_view.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class UserPasswordChangeView(PasswordChangeView):
    template_name ='users/password_change.html'


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }')
            #login the user
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('blog-homepage')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',  {'form': form})

@login_required
def profile(request):
    if request.method == "POST":

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        if u_form.has_changed() or p_form.has_changed():
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your account has been updated.')
        return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user':request.user.profile,
                                                    'user_form': u_form,
                                                    'profile_form': p_form})

