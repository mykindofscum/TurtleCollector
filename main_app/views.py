from django.shortcuts import render, redirect
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

def add_feeding(request, turtle_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.turtle_id = turtle_id
        new_feeding.save()
    return redirect('detail', turtle_id=turtle_id)
    