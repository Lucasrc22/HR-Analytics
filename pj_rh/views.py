import os

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pj_rh.models import Prestador
from pj_rh.forms import PrestadorForm
from django.urls import reverse, reverse_lazy


class PJListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Prestador
    template_name = "pj.html"
    context_object_name = "prestadores"
    permission_required = "pj_rh.view_prestador"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome_funcionario__icontains=search) | \
                       queryset.filter(nome_empresa__icontains=search)
        return queryset


class PJDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Prestador
    template_name = "pj_detail.html"
    permission_required = "pj_rh.view_prestador"


class NewPJCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Prestador
    form_class = PrestadorForm
    template_name = "new_pj.html"
    success_url = "/pj/"
    permission_required = "pj_rh.add_prestador"


class PJUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Prestador
    form_class = PrestadorForm
    template_name = "pj_update.html"
    permission_required = "pj_rh.change_prestador"

    def get_success_url(self):
        return reverse_lazy("pj_detail", kwargs={"pk": self.object.pk})


class PJDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Prestador
    template_name = "pj_delete.html"
    success_url = "/pj/"
    permission_required = "pj_rh.delete_prestador"


# Colunas exportadas: campo do model -> cabeçalho amigável no Excel.
EXPORT_COLUNAS = {
    "nome_empresa": "Nome da empresa",
    "nome_funcionario": "Nome do funcionário",
    "cargo": "Cargo",
    "setor": "Setor",
    "data_admissao": "Data de admissão",
    "data_demissao": "Data de demissão",
}


def buscar_dados_pj():
    """Gera um .xlsx com toda a base de prestadores no MEDIA_ROOT e devolve o nome do arquivo."""
    queryset = Prestador.objects.all().order_by("nome_empresa", "nome_funcionario")
    df = pd.DataFrame(list(queryset.values(*EXPORT_COLUNAS.keys())))
    df = df.reindex(columns=list(EXPORT_COLUNAS.keys()))
    df = df.rename(columns=EXPORT_COLUNAS)

    file_name = f"prestadores_{timezone.localtime().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    df.to_excel(os.path.join(settings.MEDIA_ROOT, file_name), index=False)
    return file_name


@login_required
@permission_required("pj_rh.view_prestador", raise_exception=True)
def exportar_pj(request):
    file_name = buscar_dados_pj()
    return HttpResponseRedirect(reverse("pj_get_file", args=[file_name]))


@login_required
@permission_required("pj_rh.view_prestador", raise_exception=True)
def pj_get_file(request, file_path):
    return render(request, "pj_get_file.html", {"file_path": file_path})


@login_required
@permission_required("pj_rh.view_prestador", raise_exception=True)
def pj_download(request, file_path):
    # basename evita path traversal: só arquivos dentro do MEDIA_ROOT.
    full_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(file_path))
    if os.path.exists(full_path):
        with open(full_path, "rb") as fh:
            response = HttpResponse(
                fh.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=" + os.path.basename(full_path)
            return response
    raise Http404
