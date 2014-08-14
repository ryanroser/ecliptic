from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Study(models.Model):
    name = models.CharField(max_length=30)
    hypothesis = models.CharField(max_length=300)
    conclusion = models.CharField(max_length=300, blank=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('study_detail', kwargs={'pk': self.pk})

    def __unicode__(self):  
        return self.name
