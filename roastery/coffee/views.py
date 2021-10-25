from django.views.generic import CreateView, DetailView, ListView

from .models import Bean


class BeanListView(ListView):
    model = Bean


class BeanDetailView(DetailView):
    model = Bean


class BeanCreateView(CreateView):
    model = Bean
    fields = ["name", "country"]
