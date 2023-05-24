from django import forms
from authentication.models import CustomUser, HitmanProfile


class HitmanAssignationForm(forms.Form):
    user = forms.ModelChoiceField(CustomUser.objects.filter(role__pk=3, is_active=True))
    supervisor = forms.ModelChoiceField(CustomUser.objects.filter(role__pk=2, is_active=True))



class HitCreation(forms.Form):
    target_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=100)
    