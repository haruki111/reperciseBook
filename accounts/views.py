from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from allauth.account import views
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
from .forms import ProfileForm, SignupUserForm, LoginUserForm

from .models import User


class SignupView(views.SignupView):
    template_name = 'registration/signup.html'
    form_class = SignupUserForm


class LoginView(views.LoginView):
    template_name = 'registration/login.html'
    form_class = LoginUserForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'registration/profile.html')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile_edit.html'
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user
