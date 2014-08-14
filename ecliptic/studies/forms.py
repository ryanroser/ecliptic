from django import forms
from studies.models import Study 

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study 
        fields = ['name', 'hypothesis', 'conclusion',]
