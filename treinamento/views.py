import os

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


# Colunas exportadas: campo do model -> cabeçalho amigável no Excel.
EXPORT_COLUNAS = {
    "area": "Área",
    "treinamento": "Treinamento",
    "participante": "Participante",
    "carga_horaria": "Carga Horária",
    "programado": "Programado",
    "realizado": "Realizado",
    "reprogramado": "Reprogramado",
    "cancelado": "Cancelado",
    "nenhuma_alternativa": "Nenhuma Alternativa",
    "sem_data_prevista": "Sem Data Prevista",
    "nao_realizado": "Não Realizado",
    "data_inicio": "Data de Início",
    "data_fim_planejada": "Data de Fim Planejada",
    "data_realizada": "Data Realizada",
}


def buscar_dados_treinamento():
    """Gera um .xlsx com toda a base de treinamentos no MEDIA_ROOT e devolve o nome do arquivo."""
    queryset = Treinamento.objects.all().order_by("area", "treinamento")
    df = pd.DataFrame(list(queryset.values(*EXPORT_COLUNAS.keys())))

    # Garante todas as colunas mesmo com a base vazia, e aplica os cabeçalhos.
    df = df.reindex(columns=list(EXPORT_COLUNAS.keys()))
    df = df.rename(columns=EXPORT_COLUNAS)

    # Timestamp evita sobrescrita entre exports e cache no navegador.
    file_name = f"treinamentos_{timezone.localtime().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    df.to_excel(os.path.join(settings.MEDIA_ROOT, file_name), index=False)
    return file_name


@login_required
@permission_required("treinamento.view_treinamento", raise_exception=True)
def exportar_treinamento(request):
    file_name = buscar_dados_treinamento()
    return HttpResponseRedirect(reverse("treinamento_get_file", args=[file_name]))


@login_required
@permission_required("treinamento.view_treinamento", raise_exception=True)
def treinamento_get_file(request, file_path):
    return render(request, "treinamento_get_file.html", {"file_path": file_path})


@login_required
@permission_required("treinamento.view_treinamento", raise_exception=True)
def treinamento_download(request, file_path):
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