import django.forms as forms
from decouple import config
from django.db import connection
from django.utils.html import format_html, format_html_join

from .models import Treinamento

# Configurações de banco de dados (app/settings.py)
SQL_FUNCIONARIOS_ATIVOS = config("SQL_FUNCIONARIOS_ATIVOS")


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
