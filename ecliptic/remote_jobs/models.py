from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from studies.models import Study

from remote_jobs.tasks import remote_query
from ecliptic import celery_app


# Create your models here.
class RemoteJobType(models.Model):
    name = models.CharField(max_length=30)
    create_dt = models.DateTimeField(auto_now=True)

    def __unicode__(self):  
        return self.name

class RemoteJob(models.Model):
    name = models.CharField(max_length=30)
    study = models.ForeignKey(Study)
    status = models.CharField(max_length=20, blank=True, null=True)
    job_type = models.ForeignKey(RemoteJobType)
    job_id = models.IntegerField(blank=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def get_job_and_celery(self):
        job = None
        celery = None

        job_type_name = self.job_type.name
        if job_type_name == "Remote Query":
            job = RemoteQuery.objects.get(pk=self.job_id)
        
        if job is not None:
            celery = celery_app.AsyncResult(job.celery_job)

        return [job, celery, ]

    def get_status(self):

        latest_status = self.status

        if latest_status not in ["SUCCESS", "FAILURE",]:
            # SUCCESS and FAILURE are final states, so use that value as-is.
            # Otherwise, the status is not final. We need to check the celery task and get the most recent status
            _, celery = self.get_job_and_celery()
            if celery is not None:
                celery_status = celery.status
                if celery_status != latest_status:
                    # the state has changed, update the object and latest_status to reflect the celery status
                    self.status = celery_status
                    self.save()
                    latest_status = celery_status

        return latest_status

    def get_absolute_url(self):
        return reverse('remote_job_detail', kwargs={'pk': self.pk})

    def __unicode__(self):  
        return "%s:%s" % (self.name, self.pk,)

class RemoteQuery(models.Model):
    host = models.CharField(max_length=100)
    username = models.TextField(max_length=50)
    password = models.TextField(max_length=255)
    query = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    celery_job = models.CharField(max_length=100, blank=True, null=True)
    create_dt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    def queue_job(self):
        celery_id = remote_query.delay(self.host, self.username, self.password, self.query, self.params)
        return celery_id

    def get_absolute_url(self):
        return reverse('remote_query_detail', kwargs={'pk': self.pk})

    def __unicode__(self):  
        return "RQuery: %s" % (self.pk,)


