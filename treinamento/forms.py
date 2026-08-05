import django.forms as forms
from decouple import config
from django.db import connection
from django.utils.html import format_html, format_html_join

from .models import Treinamento


_SQL_FUNCIONARIOS_ATIVOS_FALLBACK = (
    "SELECT nome FROM ("
    "SELECT DISTINCT CAST(UPPER(func.nom_pessoa_fisic) AS VARCHAR2(200)) AS nome "
    "FROM hcm.funcionario func "
    "WHERE func.dat_desligto_func IS NULL "
    "AND func.idi_tip_func NOT IN (7, 2) "
    "AND func.nom_pessoa_fisic IS NOT NULL "
    "UNION "
    "SELECT DISTINCT CAST(UPPER(pj.nome_funcionario) AS VARCHAR2(200)) AS nome "
    "FROM pbi.pj_rh_prestador pj "
    "WHERE pj.data_demissao IS NULL "
    "AND pj.nome_funcionario IS NOT NULL"
    ") ORDER BY nome"
)

SQL_FUNCIONARIOS_ATIVOS = config(
    "SQL_FUNCIONARIOS_ATIVOS", default=_SQL_FUNCIONARIOS_ATIVOS_FALLBACK
)


_SQL_EMPRESA_DO_FUNCIONARIO_FALLBACK = (
    "SELECT TRIM(REPLACE(v.nome_empresa, CHR(160), ' ')) AS nome_empresa "
    "FROM pbi.pbi_funcionarios_rh v "
    "WHERE v.data_demissao IS NULL "
    "AND UPPER(TRIM(REPLACE(v.nome_funcionario, CHR(160), ' '))) = "
    "UPPER(TRIM(REPLACE(%s, CHR(160), ' '))) "
    "ORDER BY v.data_admissao DESC NULLS LAST "
    "FETCH FIRST 1 ROW ONLY"
)

_SQL_SETOR_DO_FUNCIONARIO_FALLBACK = (
    "SELECT TRIM(REPLACE(v.setor, CHR(160), ' ')) AS setor "
    "FROM pbi.pbi_funcionarios_rh v "
    "WHERE v.data_demissao IS NULL "
    "AND UPPER(TRIM(REPLACE(v.nome_funcionario, CHR(160), ' '))) = "
    "UPPER(TRIM(REPLACE(%s, CHR(160), ' '))) "
    "ORDER BY v.data_admissao DESC NULLS LAST "
    "FETCH FIRST 1 ROW ONLY"
)

SQL_EMPRESA_DO_FUNCIONARIO = config(
    "SQL_EMPRESA_DO_FUNCIONARIO", default=_SQL_EMPRESA_DO_FUNCIONARIO_FALLBACK
)
SQL_SETOR_DO_FUNCIONARIO = config(
    "SQL_SETOR_DO_FUNCIONARIO", default=_SQL_SETOR_DO_FUNCIONARIO_FALLBACK
)


def listar_funcionarios():
    with connection.cursor() as cursor:
        cursor.execute(SQL_FUNCIONARIOS_ATIVOS)
        return [row[0] for row in cursor.fetchall()]


def buscar_empresa_setor(nome):
    nome = (nome or "").strip()
    if not nome:
        return {}

    with connection.cursor() as cursor:
        cursor.execute(SQL_EMPRESA_DO_FUNCIONARIO, [nome])
        row = cursor.fetchone()
        empresa = row[0] if row else ""

        cursor.execute(SQL_SETOR_DO_FUNCIONARIO, [nome])
        row = cursor.fetchone()
        setor = row[0] if row else ""

    if not empresa and not setor:
        return {}
    return {"empresa": empresa or "", "setor": setor or ""}


class DataListInput(forms.TextInput):

    def __init__(self, data_list, list_id, attrs=None):
        super().__init__(attrs)
        self.data_list = data_list
        self.list_id = list_id
        self.attrs.setdefault("list", list_id)
        self.attrs.setdefault("autocomplete", "off")

    def render(self, name, value, attrs=None, renderer=None):
        text_input = super().render(name, value, attrs, renderer)
        options = format_html_join(
            "", "<option value=\"{}\">", ((item,) for item in self.data_list)
        )
        datalist = format_html('<datalist id="{}">{}</datalist>', self.list_id, options)
        return format_html("{}{}", text_input, datalist)


class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = Treinamento
        fields = "__all__"
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim_planejada": forms.DateInput(attrs={"type": "date"}),
            "data_realizada": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nomes = listar_funcionarios()
        self.fields["funcionario"] = forms.CharField(
            label="Funcionário",
            max_length=100,
            widget=DataListInput(
                data_list=nomes,
                list_id="funcionarios_datalist",
                attrs={"placeholder": "Digite o nome do funcionário..."},
            ),
        )
