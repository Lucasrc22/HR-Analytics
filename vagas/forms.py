import django.forms as forms
from decouple import config
from django.db import connection
from django.utils.html import format_html, format_html_join
from vagas.models import Vagas

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

def listar_funcionarios():
    with connection.cursor() as cursor:
        cursor.execute(SQL_FUNCIONARIOS_ATIVOS)
        return [row[0] for row in cursor.fetchall()]


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


class VagasForm(forms.ModelForm):
    class Meta:
        model = Vagas
        fields = "__all__"
        widgets = {
            "data_abertura": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "data_fechamento": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "previsao_admissao": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            nomes = listar_funcionarios()
            self.fields["nom_funcionario"] = forms.CharField(
                label="Funcionário",
                max_length=100,
                widget=DataListInput(
                    data_list=nomes, 
                    list_id="funcionarios-list",
                    attrs = {"placeholder": "Digite o nome do funcionário"},
                ),
            )