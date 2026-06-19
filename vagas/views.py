import os

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
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


# Colunas exportadas: campo do model -> cabeçalho amigável no Excel.
EXPORT_COLUNAS = {
    "empresa": "Empresa",
    "sigiloso": "Sigiloso",
    "tipo_vaga": "Tipo de Vaga",
    "consultoria": "Consultoria",
    "area": "Área",
    "quantidade": "Quantidade",
    "data_abertura": "Data de Abertura",
    "data_fechamento": "Data de Fechamento",
    "cargo": "Cargo",
    "status": "Status",
    "motivo": "Motivo",
    "justificativa": "Justificativa",
    "nome_candidato": "Nome do Candidato",
    "previsao_admissao": "Previsão de Admissão",
    "observacoes": "Observações",
}


def buscar_dados_vagas():
    """Gera um .xlsx com toda a base de vagas no MEDIA_ROOT e devolve o nome do arquivo."""
    queryset = Vagas.objects.all().order_by("empresa", "cargo")
    df = pd.DataFrame(list(queryset.values(*EXPORT_COLUNAS.keys())))
    df = df.reindex(columns=list(EXPORT_COLUNAS.keys()))
    df = df.rename(columns=EXPORT_COLUNAS)

    file_name = f"vagas_{timezone.localtime().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    df.to_excel(os.path.join(settings.MEDIA_ROOT, file_name), index=False)
    return file_name


@login_required
@permission_required("vagas.view_vagas", raise_exception=True)
def exportar_vagas(request):
    file_name = buscar_dados_vagas()
    return HttpResponseRedirect(reverse("vagas_get_file", args=[file_name]))


@login_required
@permission_required("vagas.view_vagas", raise_exception=True)
def vagas_get_file(request, file_path):
    return render(request, "vagas_get_file.html", {"file_path": file_path})


@login_required
@permission_required("vagas.view_vagas", raise_exception=True)
def vagas_download(request, file_path):
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