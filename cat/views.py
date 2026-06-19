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
from .models import CAT
from .forms import CATForm


class CATListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CAT
    template_name = "cat.html"
    context_object_name = "cats"
    permission_required = "cat.view_cat"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-dat_afast_func_acidte")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(nom_funcionario__icontains=search)
        return queryset


class CATDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CAT
    template_name = "cat_detail.html"
    context_object_name = "cat"
    permission_required = "cat.view_cat"


class NewCATCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CAT
    template_name = "new_cat.html"
    form_class = CATForm
    success_url = "/cat/"
    permission_required = "cat.add_cat"


class CATUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CAT
    template_name = "cat_update.html"
    form_class = CATForm
    permission_required = "cat.change_cat"

    def get_success_url(self):
        return reverse_lazy("cat_detail", kwargs={"pk": self.object.pk})


class CATDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CAT
    template_name = "cat_delete.html"
    success_url = reverse_lazy("cat_list")
    permission_required = "cat.delete_cat"


# Colunas exportadas: campo do model -> cabeçalho amigável no Excel.
EXPORT_COLUNAS = {
    "nom_empresa": "Nome da empresa",
    "matricula": "Matrícula",
    "nom_funcionario": "Nome do funcionário",
    "setor": "Setor",
    "acidente": "Acidente",
    "dat_afast_func_acidte": "Data do acidente",
}


def buscar_dados_cat():
    """Gera um .xlsx com toda a base de CATs no MEDIA_ROOT e devolve o nome do arquivo."""
    queryset = CAT.objects.all().order_by("-dat_afast_func_acidte")
    df = pd.DataFrame(list(queryset.values(*EXPORT_COLUNAS.keys())))
    df = df.reindex(columns=list(EXPORT_COLUNAS.keys()))
    df = df.rename(columns=EXPORT_COLUNAS)

    file_name = f"cat_{timezone.localtime().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    df.to_excel(os.path.join(settings.MEDIA_ROOT, file_name), index=False)
    return file_name


@login_required
@permission_required("cat.view_cat", raise_exception=True)
def exportar_cat(request):
    file_name = buscar_dados_cat()
    return HttpResponseRedirect(reverse("cat_get_file", args=[file_name]))


@login_required
@permission_required("cat.view_cat", raise_exception=True)
def cat_get_file(request, file_path):
    return render(request, "cat_get_file.html", {"file_path": file_path})


@login_required
@permission_required("cat.view_cat", raise_exception=True)
def cat_download(request, file_path):
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
