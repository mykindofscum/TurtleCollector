from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3
from .models import Turtle, Photo, Toy
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'turtlecollector'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class TurtleUpdate(LoginRequiredMixin, UpdateView):
    model = Turtle
    fields = ['breed', 'description', 'age']

class TurtleDelete(LoginRequiredMixin, DeleteView):
    model = Turtle
    success_url = '/turtles/'

class TurtleCreate(LoginRequiredMixin, CreateView):
    model = Turtle
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def turtles_index(request):
    turtles = Turtle.objects.filter(user=request.user)
    return render(request, 'turtles/index.html', { 'turtles': turtles })

@login_required
def turtles_detail(request, turtle_id):
    turtle = Turtle.objects.get(id=turtle_id)
    toys_turtle_doesnt_have = Toy.objects.exclude(id__in = turtle.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'turtles/detail.html', {
         'turtle': turtle, 'toys': toys_turtle_doesnt_have, 'feeding_form': feeding_form 
    })

@login_required
def add_feeding(request, turtle_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.turtle_id = turtle_id
        new_feeding.save()
    return redirect('detail', turtle_id=turtle_id)

@login_required
def add_photo(request, turtle_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3') 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, turtle_id=turtle_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', turtle_id=turtle_id)

@login_required
def assoc_toy(request, turtles_id, toy_id):
    Turtle.objects.get(id=turtles_id).toys.add(toy_id)
    return redirect('detail', turtles_id)

@login_required
def unassoc_toy(request, turtles_id, toy_id):
    Turtle.objects.get(id=turtles_id).toys.remove(toy_id)
    return redirect('detail', turtles_id)

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']
    
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'