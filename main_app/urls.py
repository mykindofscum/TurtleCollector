from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('about/', views.about, name='about'),
    path('turtles/', views.turtles_index, name='index'),
    path('turtles/<int:turtle_id>/', views.turtles_detail, name='detail'),
    path('turtles/create/', views.TurtleCreate.as_view(), name='turtles_create'),
    path('turtles/<int:pk>/update/', views.TurtleUpdate.as_view(), name='turtles_update'),
    path('turtles/<int:pk>/delete/', views.TurtleDelete.as_view(), name='turtles_delete'),
    path('turtles/<int:turtle_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('turtles/<int:turtles_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('turtles/<int:turtles_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('turtles/<int:turtle_id>/add_photo/', views.add_photo, name='add_photo'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('accounts/signup', views.signup, name='signup'),
]