from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import DeleteView

from .forms import RoastForm
from .models import Bean, Extraction, Roast

# CUSTOM MIXINS


class LoginRequiredWithErrorMessageMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# HOME VIEW
class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["bean_count"] = Bean.objects.count()
        context["roast_count"] = Roast.objects.count()
        context["extraction_count"] = Extraction.objects.count()
        return context


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
    fields = ["green_bean", "degree", "green_weight", "roasted_weight"]
    permission_denied_message = "You're not allowed on this page without an account"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.current_weight = (
            form.instance.roasted_weight
        )  # set current weight to the roasted weight
        return super().form_valid(form)


class RoastUpdateView(UserPassesTestMixin, UpdateView):
    model = Roast
    form_class = RoastForm
    permission_denied_message = "You can't make updates from this account"
    action = "Update"
    bootstrap_class = "warning"

    def test_func(self):
        return self.request.user == self.get_object().created_by


class RoastDeleteView(LoginRequiredWithErrorMessageMixin, DeleteView):
    model = Roast
    success_url = reverse_lazy("coffee:roast-list")


# EXTRACTION VIEWS


class ExtractionListView(ListView):
    model = Extraction


class ExtractionDetailView(DetailView):
    model = Extraction


class ExtractionCreateView(LoginRequiredWithErrorMessageMixin, CreateView):
    model = Extraction
    fields = [
        "roasted_bean",
        "method",
        "dose",
        "grinder",
        "grind_setting",
        "temperature",
        "notes",
    ]
    permission_denied_message = "You're not allowed on this page without an account"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        print("dose", form.instance.dose)
        current_weight_error = form.instance.roasted_bean.decrement(form.instance.dose)
        if current_weight_error:
            response = super().form_invalid(form)
            messages.warning(
                self.request,
                f"Only {current_weight_error} g of beans; select a smaller dose",
            )
            if self.request.accepts("text/html"):
                return response
        return super().form_valid(form)


class ExtractionUpdateView(UserPassesTestMixin, UpdateView):
    model = Extraction
    fields = [
        "roasted_bean",
        "method",
        "dose",
        "grinder",
        "grind_setting",
        "temperature",
        "notes",
    ]
    permission_denied_message = "You can't make updates from this account"
    action = "Update"
    bootstrap_class = "warning"

    def test_func(self):
        return self.request.user == self.get_object().created_by


class ExtractionDeleteView(LoginRequiredWithErrorMessageMixin, DeleteView):
    model = Extraction
    success_url = reverse_lazy("coffee:extraction-list")
