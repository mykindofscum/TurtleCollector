from django.shortcuts import render
from .models import Turtle


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def turtles_index(request):
    turtles = Turtle.objects.all()
    return render(request, 'turtles/index.html', { 'turtles': turtles })

def turtles_detail(request, turtle_id):
    turtle = Turtle.objects.get(id=turtle_id)
    return render(request, 'turtles/detail.html', { 'turtle': turtle })
    