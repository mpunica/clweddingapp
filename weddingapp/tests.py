from django.test import TestCase, Client
from .models import Guest, BrideGroom
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pytest


class AppTestCase(TestCase):
    def test_app_get(self):
        response = self.client.get('/', INSTALLES_APPS='weddingapp')
        self.assertEqual(response.status_code, 200)

def test_main_page():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200
    assert "Bride&Groom - WeddingApp" in str(response.content, "utf-8")

def test_login_view():
    c = Client()
    response = c.get('/login/')
    assert response.status_code == 200

def test_login_view2():
    c = Client()
    response = c.post('/login/', {'username': 'user111', 'password': 'user111'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_view():
    u = User.objects.create_user(username="user111", password="user111")
    c = Client()
    c.login(username="user111", password="user111")
    response = c.get('/logout/', )
    c.logout()
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_bridegroom1():
    u = User.objects.create_user(username="admin", password="admin", is_superuser=True)
    c = Client()
    c.login(username="admin", password="admin")
    response = c.get('/add_bridegroom/', )
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_bridegroom2():
    u = User.objects.create_user(username="admin", password="admin", is_superuser=True)
    assert len(BrideGroom.objects.all()) == 0
    c = Client()
    c.login(username="admin", password="admin")
    response = c.post('/add_bridegroom/',
                      {"name": "paniM", "BrideGroom": "0"}, follow=True)
    assert response.status_code == 200
    assert len(BrideGroom.objects.all()) == 1

@pytest.mark.django_db
def test_post_endpoint():
    u = User.objects.create_user(username="user222", password="user222")
    c = Client()
    c.login(username="user222", password="user222")
    response = c.get('/logout/',
                      {"username": "user222", "password":"user222"}, enforce_csrf_checks=True)
    assert response.status_code == 200

