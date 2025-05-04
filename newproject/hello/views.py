from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def map_view(request):
    return render(request, 'map.html')

def categories(request):
    return render(request, 'categories.html')

def catalog(request):
    return render(request, 'catalog.html')

def cart(request):
    return render(request, 'cart.html')



class MusicListView(ListView):
        model = Music
        template_name = 'music/music_list.html'
        context_object_name = 'music'   


class MusicDetailView(DetailView):
        model = Music
        template_name = 'music/music_detail.html'
        context_object_name = 'music'   

from .forms import MusicForm

class MusicCreateView(CreateView):
    model = Music
    form_class = MusicForm
    template_name = 'music/music_forms.html'
    success_url = reverse_lazy('music_list')


class MusicUpdateView(UpdateView):
        model = Music
        form_class = MusicForm
        template_name = 'music/music_forms.html'
        context_object_name = reverse_lazy ('music_list') 

class MusicDeleteView(DeleteView):
        model = Music
        template_name = 'music/music_delete.html'
        context_object_name = reverse_lazy ('music_list')