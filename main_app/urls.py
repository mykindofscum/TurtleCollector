from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('about/', views.about, name='about'),
    path('turtles/', views.turtles_index, name='index'),
    path('turtles/<int:turtle_id>/', views.turtles_detail, name='detail')
]