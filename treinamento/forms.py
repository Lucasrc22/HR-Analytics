import django.forms as forms
from .models import Treinamento


class TreinamentoForm(forms.ModelForm):
    class Meta:
        model = Treinamento
        fields = "__all__"
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim_planejada": forms.DateInput(attrs={"type": "date"}),
            "data_realizada": forms.DateInput(attrs={"type": "date"}),
        }
