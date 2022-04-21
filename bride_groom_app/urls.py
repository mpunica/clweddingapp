"""bride_groom_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weddingapp.views import Login, Logout, AddUser, ResetPassword, AddGuestView, GuestView, MainWeddingView, AddGuestView, AddBrideGroomView, ListGuests


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainWeddingView.as_view(), name="index"),
    # path('login/', LoginView.as_view(), name="login"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('add_user/', AddUser.as_view(), name="add_user"),
    path('reset_password/<int:user_id>/', ResetPassword.as_view(), name="reset_password"),
    path('add_guest/', AddGuestView.as_view(), name="add_guest"),
    path('guest/<int:guest_id>/', GuestView.as_view(), name="guest"),
    path('list_guest/', ListGuests.as_view(), name="all_guests"),
    path('add_bridegroom/', AddBrideGroomView.as_view(), name="add_bridegroom"),
]
