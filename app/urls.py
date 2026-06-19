
from django.contrib import admin
from django.urls import path
from app.views import HomeView
from pj_rh.views import (
    NewPJCreateView,
    PJListView,
    PJDetailView,
    PJUpdateView,
    PJDeleteView,
    exportar_pj,
    pj_get_file,
    pj_download,
)
from user.views import register_view, login_view, logout_view
from cat.views import (
    CATListView,
    CATDetailView,
    NewCATCreateView,
    CATUpdateView,
    CATDeleteView,
    exportar_cat,
    cat_get_file,
    cat_download,
)
from treinamento.views import (
    TreinamentoListView,
    TreinamentoDetailView,
    NewTreinamentoCreateView,
    TreinamentoUpdateView,
    TreinamentoDeleteView,
    exportar_treinamento,
    treinamento_get_file,
    treinamento_download,
)
from vagas.views import (
    VagasListView,
    VagasDetailView,
    NewVagasCreateView,
    VagasUpdateView,
    VagasDeleteView,
    exportar_vagas,
    vagas_get_file,
    vagas_download,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('cat/', CATListView.as_view(), name='cat_list'),
    path('cat/<int:pk>/', CATDetailView.as_view(), name='cat_detail'),
    path('cat/new/', NewCATCreateView.as_view(), name='new_cat'),
    path('cat/<int:pk>/edit/', CATUpdateView.as_view(), name='cat_update'),
    path('cat/<int:pk>/delete/', CATDeleteView.as_view(), name='cat_delete'),
    path('cat/export/', exportar_cat, name='cat_export'),
    path('cat/get_file/<str:file_path>/', cat_get_file, name='cat_get_file'),
    path('cat/download/<str:file_path>/', cat_download, name='cat_download'),
    path('pj/', PJListView.as_view(), name='pj_list'),
    path('pj/<int:pk>/', PJDetailView.as_view(), name='pj_detail'),
    path('new_pj/', NewPJCreateView.as_view(), name='new_pj'),
    path('pj/<int:pk>/edit/', PJUpdateView.as_view(), name='pj_update'),
    path('pj/<int:pk>/delete/', PJDeleteView.as_view(), name='pj_delete'),
    path('pj/export/', exportar_pj, name='pj_export'),
    path('pj/get_file/<str:file_path>/', pj_get_file, name='pj_get_file'),
    path('pj/download/<str:file_path>/', pj_download, name='pj_download'),
    path('treinamento/', TreinamentoListView.as_view(), name='treinamento_list'),
    path('treinamento/<int:pk>/', TreinamentoDetailView.as_view(), name='treinamento_detail'),
    path('treinamento/new/', NewTreinamentoCreateView.as_view(), name='new_treinamento'),
    path('treinamento/<int:pk>/edit/', TreinamentoUpdateView.as_view(), name='treinamento_update'),
    path('treinamento/<int:pk>/delete/', TreinamentoDeleteView.as_view(), name='treinamento_delete'),
    path('treinamento/export/', exportar_treinamento, name='treinamento_export'),
    path('treinamento/get_file/<str:file_path>/', treinamento_get_file, name='treinamento_get_file'),
    path('treinamento/download/<str:file_path>/', treinamento_download, name='treinamento_download'),
    path('vagas/', VagasListView.as_view(), name='vagas_list'),
    path('vagas/<int:pk>/', VagasDetailView.as_view(), name='vagas_detail'),
    path('vagas/new/', NewVagasCreateView.as_view(), name='new_vagas'),
    path('vagas/<int:pk>/edit/', VagasUpdateView.as_view(), name='vagas_update'),
    path('vagas/<int:pk>/delete/', VagasDeleteView.as_view(), name='vagas_delete'),
    path('vagas/export/', exportar_vagas, name='vagas_export'),
    path('vagas/get_file/<str:file_path>/', vagas_get_file, name='vagas_get_file'),
    path('vagas/download/<str:file_path>/', vagas_download, name='vagas_download'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
