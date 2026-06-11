import django.forms as forms
from cat.models import CAT


class CATForm(forms.ModelForm):
    class Meta:
        model = CAT
        fields = "__all__"
        widgets = {
            "dat_afast_func_acidte": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }
