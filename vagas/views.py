from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Vagas
from .forms import VagasForm


class VagasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vagas
    template_name = "vagas.html"
    context_object_name = "vagas"
    permission_required = "vagas.view_vagas"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("empresa", "cargo")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(cargo__icontains=search)
        return queryset


class VagasDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Vagas
    template_name = "vagas_detail.html"
    context_object_name = "vaga"
    permission_required = "vagas.view_vagas"


class NewVagasCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Vagas
    template_name = "new_vagas.html"
    form_class = VagasForm
    success_url = "/vagas/"
    permission_required = "vagas.add_vagas"


class VagasUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Vagas
    template_name = "vagas_update.html"
    form_class = VagasForm
    permission_required = "vagas.change_vagas"

    def get_success_url(self):
        return reverse_lazy("vagas_detail", kwargs={"pk": self.object.pk})


class VagasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Vagas
    template_name = "vagas_delete.html"
    success_url = reverse_lazy("vagas_list")
    permission_required = "vagas.delete_vagas"