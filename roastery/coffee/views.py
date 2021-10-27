from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from .models import Bean


class LoginRequiredWithErrorMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BeanListView(ListView):
    model = Bean


class BeanDetailView(DetailView):
    model = Bean


class BeanCreateView(LoginRequiredWithErrorMessageMixin, CreateView):
    model = Bean
    fields = ["name", "country", "description"]
    permission_denied_message = "You're not allowed on this page without an account"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BeanUpdateView(LoginRequiredWithErrorMessageMixin, UpdateView):
    model = Bean
    fields = ["name", "country", "description"]
    permission_denied_message = "You're not allowed on this page without an account"
    action = "Update"
    bootstrap_class = "warning"


class BeanDeleteView(LoginRequiredWithErrorMessageMixin, DeleteView):
    model = Bean
    success_url = reverse_lazy("coffee:bean-list")
