from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import CAT


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
    fields = "__all__"
    success_url = "/cat/"
    permission_required = "cat.add_cat"


class CATUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CAT
    template_name = "cat_update.html"
    fields = "__all__"
    permission_required = "cat.change_cat"

    def get_success_url(self):
        return reverse_lazy("cat_detail", kwargs={"pk": self.object.pk})


class CATDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CAT
    template_name = "cat_delete.html"
    success_url = reverse_lazy("cat_list")
    permission_required = "cat.delete_cat"
