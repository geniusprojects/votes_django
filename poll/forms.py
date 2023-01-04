from django.forms import ModelForm
from django.forms.widgets import TextInput
from poll.models import Choice


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"
        widgets = {
            "color": TextInput(attrs={"type": "color"}),
        }
