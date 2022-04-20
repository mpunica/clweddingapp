from django.test import TestCase, Client
import pytest

def test_main_page():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200
    assert "Bride&Groom - WeddingApp" in str(response.content, "utf-8")

def test_login_view():
    c = Client()
    response = c.get('/login/')
    assert response.status_code == 200
