from django.urls import path
from . import views

urlpatterns = [
  path('generate/carrousel', views.generate_carrousel_content, name='generate_carrousel_content'),
]