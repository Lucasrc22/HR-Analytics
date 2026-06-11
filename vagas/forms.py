import django.forms as forms
from vagas.models import Vagas


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
