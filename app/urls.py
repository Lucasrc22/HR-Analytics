
from django.contrib import admin
from django.urls import path
from app.views import HomeView
from pj_rh.views import NewPJCreateView, PJListView, PJDetailView, PJUpdateView, PJDeleteView
from user.views import register_view, login_view, logout_view
from cat.views import (
    CATListView,
    CATDetailView,
    NewCATCreateView,
    CATUpdateView,
    CATDeleteView,
)
from treinamento.views import (
    TreinamentoListView,
    TreinamentoDetailView,
    NewTreinamentoCreateView,
    TreinamentoUpdateView,
    TreinamentoDeleteView,
)
from vagas.views import (
    VagasListView,
    VagasDetailView,
    NewVagasCreateView,
    VagasUpdateView,
    VagasDeleteView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('cat/', CATListView.as_view(), name='cat_list'),
    path('cat/<int:pk>/', CATDetailView.as_view(), name='cat_detail'),
    path('cat/new/', NewCATCreateView.as_view(), name='new_cat'),
    path('cat/<int:pk>/edit/', CATUpdateView.as_view(), name='cat_update'),
    path('cat/<int:pk>/delete/', CATDeleteView.as_view(), name='cat_delete'),
    path('pj/', PJListView.as_view(), name='pj_list'),
    path('pj/<int:pk>/', PJDetailView.as_view(), name='pj_detail'),
    path('new_pj/', NewPJCreateView.as_view(), name='new_pj'),
    path('pj/<int:pk>/edit/', PJUpdateView.as_view(), name='pj_update'),
    path('pj/<int:pk>/delete/', PJDeleteView.as_view(), name='pj_delete'),
    path('treinamento/', TreinamentoListView.as_view(), name='treinamento_list'),
    path('treinamento/<int:pk>/', TreinamentoDetailView.as_view(), name='treinamento_detail'),
    path('treinamento/new/', NewTreinamentoCreateView.as_view(), name='new_treinamento'),
    path('treinamento/<int:pk>/edit/', TreinamentoUpdateView.as_view(), name='treinamento_update'),
    path('treinamento/<int:pk>/delete/', TreinamentoDeleteView.as_view(), name='treinamento_delete'),
    path('vagas/', VagasListView.as_view(), name='vagas_list'),
    path('vagas/<int:pk>/', VagasDetailView.as_view(), name='vagas_detail'),
    path('vagas/new/', NewVagasCreateView.as_view(), name='new_vagas'),
    path('vagas/<int:pk>/edit/', VagasUpdateView.as_view(), name='vagas_update'),
    path('vagas/<int:pk>/delete/', VagasDeleteView.as_view(), name='vagas_delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
