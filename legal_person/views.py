from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from legal_person.models import Prestador
from legal_person.forms import PrestadorForm
from django.urls import reverse_lazy


class PJListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Prestador
    template_name = "pj.html"
    context_object_name = "prestadores"
    permission_required = "legal_person.view_prestador"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome_funcionario__icontains=search) | \
                       queryset.filter(nome_empresa__icontains=search) | \
                       queryset.filter(matricula__icontains=search)
        return queryset


class PJDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Prestador
    template_name = "pj_detail.html"
    permission_required = "legal_person.view_prestador"


class NewPJCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Prestador
    form_class = PrestadorForm
    template_name = "new_pj.html"
    success_url = "/pj/"
    permission_required = "legal_person.add_prestador"


class PJUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Prestador
    form_class = PrestadorForm
    template_name = "pj_update.html"
    permission_required = "legal_person.change_prestador"

    def get_success_url(self):
        return reverse_lazy("pj_detail", kwargs={"pk": self.object.pk})


class PJDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Prestador
    template_name = "pj_delete.html"
    success_url = "/pj/"
    permission_required = "legal_person.delete_prestador"
