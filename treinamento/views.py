from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Treinamento
from .forms import TreinamentoForm


class TreinamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Treinamento
    template_name = "treinamento.html"
    context_object_name = "treinamentos"
    permission_required = "treinamento.view_treinamento"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("area", "treinamento")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(treinamento__icontains=search)
        return queryset


class TreinamentoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Treinamento
    template_name = "treinamento_detail.html"
    context_object_name = "treinamento"
    permission_required = "treinamento.view_treinamento"


class NewTreinamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Treinamento
    template_name = "new_treinamento.html"
    form_class = TreinamentoForm
    success_url = "/treinamento/"
    permission_required = "treinamento.add_treinamento"


class TreinamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Treinamento
    template_name = "treinamento_update.html"
    form_class = TreinamentoForm
    permission_required = "treinamento.change_treinamento"

    def get_success_url(self):
        return reverse_lazy("treinamento_detail", kwargs={"pk": self.object.pk})


class TreinamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Treinamento
    template_name = "treinamento_delete.html"
    success_url = reverse_lazy("treinamento_list")
    permission_required = "treinamento.delete_treinamento"