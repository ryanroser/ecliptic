from django import forms
from remote_jobs.models import RemoteJob

class RemoteJobForm(forms.ModelForm):
    class Meta:
        model = RemoteJob
        fields = ['name', 'study', 'job_type', ]
