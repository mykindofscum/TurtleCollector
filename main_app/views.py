from django.shortcuts import render, redirect
from .models import Turtle, Photo, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'turtlecollector'

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

class ToyList(ListView):
    model = Toy

class ToyDetail(CreateView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color'
    
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
