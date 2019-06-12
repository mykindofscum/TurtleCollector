from django.shortcuts import render
from .models import Turtle
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm

class TurtleUpdate(UpdateView):
    model = Turtle
    fields = ['breed', 'description', 'age']

class TurtleDelete(DeleteView):
    model = Turtle
    success_url = '/turtles/'

class TurtleCreate(CreateView):
    model = Turtle
    fields = '__all__'
    success_url = '/turtles/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def turtles_index(request):
    turtles = Turtle.objects.all()
    return render(request, 'turtles/index.html', { 'turtles': turtles })

def turtles_detail(request, turtle_id):
    turtle = Turtle.objects.get(id=turtle_id)
    feeding_form = FeedingForm()
    return render(request, 'turtles/detail.html', {
         'turtle': turtle, 'feeding_form': feeding_form 
    })
    