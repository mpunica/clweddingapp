from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import (
    LoginForm,
    UserForm,
    AddUserForm,
    ResetPasswordForm,
    AddGuestForm,
)

from .models import BrideGroom_choice, BrideGroom, Guest, Present, SeatTable, Messages

# class MainWeddingView(View):
#     # jakiś widok na początek
#     def get(self, request):
#         ctx = {"school_classes": SCHOOL_CLASS}
#         return render(request, "index.html", ctx)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {"form": form}

        if form.is_valid():
            if (
                form.cleaned_data["login"] == "root"
                and form.cleaned_data["password"] == "very_secret"
            ):
                return HttpResponse("Miło Cię widzieć")
            return HttpResponse("Błąd logowania")
        return render(request, "login_form.html", ctx)

class Login(FormView):
    form_class = LoginForm
    template_name = "login_form.html"

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["login"], password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("Błąd logowania")
        return redirect(reverse("index"))


class Logout(View):
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        return redirect(reverse("index"))

class AddUser(CreateView):
    form_class = AddUserForm
    template_name = "add_user.html"
    success_url = reverse_lazy("index")

class ResetPassword(PermissionRequiredMixin, FormView):
    permission_required = "auth.change_user"
    form_class = ResetPasswordForm
    template_name = "reset_password.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        password_owner = get_object_or_404(User, id=self.kwargs.get('user_id'))
        ctx["password_owner"] = password_owner
        return ctx

    def form_valid(self, form):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.set_password(form.cleaned_data['password_1'])
        user.save()
        return redirect(self.success_url)

class AddGuestView(FormView):
    form_class = AddGuestForm
    template_name = "add_guest.html"

    def form_valid(self, form):
        new_student = Student.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            school_class=form.cleaned_data["school_class"],
            year_of_birth=form.cleaned_data["year_of_birth"],
        )

        self.success_url = f"/student/{new_student.id}"
        return super().form_valid(form)