from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, UpdateView


from .forms import CustomUserCreationForm
from .models import Profile
class RegisterView(FormView):
    """
    Managing registration of new users

    Attributes:
     - email: User's valid email address
     - password1: User's password
     - password2: User's password confirmation
    """

    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # login user after successful registration
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
