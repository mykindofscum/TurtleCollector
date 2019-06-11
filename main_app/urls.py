from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('about/', views.about, name='about'),
    path('turtles/', views.turtles_index, name='index'),
    path('turtles/<int:turtle_id>/', views.turtles_detail, name='detail'),
    path('turtles/create/', views.TurtleCreate.as_view(), name='turtles_create'),
    path('turtles/<int:pk>/update/', views.TurtleUpdate.as_view(), name='turtles_update'),
    path('turtles/<int:pk>/delete/', views.TurtleDelete.as_view(), name='turtles_delete'),
]