from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from .models import Bean, Roast

# CUSTOM MIXINS


class LoginRequiredWithErrorMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# BEAN VIEWS


class BeanListView(ListView):
    model = Bean

    def get_ordering(self):
        return self.request.GET.get("sort")


class BeanDetailView(DetailView):
    model = Bean


class BeanCreateView(LoginRequiredWithErrorMessageMixin, CreateView):
    model = Bean
    fields = ["name", "country", "description"]
    permission_denied_message = "You're not allowed on this page without an account"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BeanUpdateView(UserPassesTestMixin, UpdateView):
    model = Bean
    fields = ["name", "country", "description"]
    permission_denied_message = "You can't make updates from this account"
    action = "Update"
    bootstrap_class = "warning"

    def test_func(self):
        return self.request.user == self.get_object().created_by


class BeanDeleteView(LoginRequiredWithErrorMessageMixin, DeleteView):
    model = Bean
    success_url = reverse_lazy("coffee:bean-list")


# ROAST VIEWS


class RoastListView(ListView):
    model = Roast


class RoastDetailView(DetailView):
    model = Roast


class RoastCreateView(LoginRequiredWithErrorMessageMixin, CreateView):
    model = Roast
    fields = ["green_bean", "degree"]
    permission_denied_message = "You're not allowed on this page without an account"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RoastUpdateView(UserPassesTestMixin, UpdateView):
    model = Roast
    fields = ["green_bean", "degree"]
    permission_denied_message = "You can't make updates from this account"
    action = "Update"
    bootstrap_class = "warning"

    def test_func(self):
        return self.request.user == self.get_object().created_by


class RoastDeleteView(LoginRequiredWithErrorMessageMixin, DeleteView):
    model = Roast
    success_url = reverse_lazy("coffee:roast-list")
