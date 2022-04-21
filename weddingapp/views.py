"""
Django views for coderslab app.
"""
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import (
    LoginForm,
    UserForm,
    AddUserForm,
    ResetPasswordForm,
    AddGuestForm,
    AddBrideGroomForm,
)

from .models import BrideGroom_choice, BrideGroom, Guest, Present, SeatTable, Messages

class MainWeddingView(View):
    """
    Main view
    """
    def get(self, request):
        return render(request, "index.html")
#     def get(self, request):
#         ctx = {"school_classes": SCHOOL_CLASS}
#         return render(request, "index.html", ctx)


class SuperUserCheck(UserPassesTestMixin):
    '''
    Check if user is a superuser
    '''
    def test_func(self):
        return self.request.user.is_superuser

# class LoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, "login_form.html", {"form": form})
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         ctx = {"form": form}
#
#         if form.is_valid():
#             if (
#                 form.cleaned_data["login"] == "root"
#                 and form.cleaned_data["password"] == "very_secret"
#             ):
#                 return HttpResponse("Miło Cię widzieć")
#             return HttpResponse("Błąd logowania")
#         return render(request, "login_form.html", ctx)

class Login(FormView):
    """
    Login view
    """
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


class Logout(LoginRequiredMixin, View):
    """
    Logout view
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        return redirect(reverse("index"))

class AddUser(LoginRequiredMixin, CreateView):
    """
    Add new user
    """
    login_url = '/login/'
    form_class = AddUserForm
    template_name = "add_user.html"
    success_url = reverse_lazy("index")

class ResetPassword(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """
    Reset users password
    """
    permission_required = "auth.change_user"
    form_class = ResetPasswordForm
    template_name = "reset_password.html"
    success_url = reverse_lazy("index")
    login_url = '/login/'

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

class AddBrideGroomView(SuperUserCheck, FormView):
    """
    Add names of Bride and Groom
    """
    form_class = AddBrideGroomForm
    template_name = "add_bridegroom.html"

    def form_valid(self, form):
        new_bridegroom = BrideGroom.objects.create(
        name=form.cleaned_data["name"],
        BrideGroom=form.cleaned_data["BrideGroom"],
        )

        self.success_url = f"/"
        return super().form_valid(form)

class AddGuestView(SuperUserCheck, FormView):
    """
    Add new guest
    """
    form_class = AddGuestForm
    template_name = "add_guest.html"

    def form_valid(self, form):
        # bridegrooms = BrideGroom.objects.get(pk=form.cleaned_data['bridegrooms'])
        new_guest = Guest.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            is_child=form.cleaned_data["is_child"],
            bridegrooms=form.cleaned_data["bridegrooms"],
            in_confirmed=form.cleaned_data["in_confirmed"],
        )

        self.success_url = f"/guest/{new_guest.id}"
        return super().form_valid(form)

class GuestView(LoginRequiredMixin, View):
    """
    Generate guest view
    """
    def get(self, request, guest_id):
        ctx = {}
        ctx["guest"] = get_object_or_404(Guest, pk=guest_id)
        ctx["bridegrooms"] = BrideGroom.objects.order_by("name").all()
        ctx["presents"] = Present.objects.order_by("present_name").all()
        ctx["seattables"] = SeatTable.objects.order_by("table_nr").all()
        return render(request, "guest.html", ctx)

class ListGuests(SuperUserCheck, TemplateView):
    """
    Generate guests list
    """
    template_name = "all_guests.html"

    def get_context_data(self):
        return {"guests": Guest.objects.all()}