from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('success/', views.success_page, name='success'),
]
