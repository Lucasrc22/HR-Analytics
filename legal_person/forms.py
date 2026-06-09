import django.forms as forms
from legal_person.models import Prestador


class PrestadorForm(forms.ModelForm):
    class Meta:
        model = Prestador
        fields = [
            "nome_empresa",
            "matricula",
            "nome_funcionario",
            "setor",
            "data_admissao",
            "data_demissao",
        ]
        widgets = {
            "data_admissao": forms.DateInput(attrs={"type": "date"}),
            "data_demissao": forms.DateInput(attrs={"type": "date"}),
        }
