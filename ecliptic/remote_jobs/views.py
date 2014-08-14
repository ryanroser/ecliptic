from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from remote_jobs.models import RemoteJob, RemoteQuery
from remote_jobs.forms import RemoteJobForm

from ecliptic import celery_app



class RemoteJobList(ListView):
    model = RemoteJob
    template_name = 'remote_jobs/remote_job_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RemoteJobList, self).dispatch(*args, **kwargs)

class RemoteJobDetail(DetailView):
    model = RemoteJob
    template_name = 'remote_jobs/remote_job_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RemoteJobDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RemoteJobDetail, self).get_context_data(**kwargs)

        context_object = context['object']
        job, celery = context_object.get_job_and_celery()
        context['job'] = job
        context['celery'] = celery

        return context

class RemoteJobCreate(CreateView):
    form_class = RemoteJobForm
    template_name = 'remote_jobs/remote_job_add.html'
    model = RemoteJob
    fields = ['name', 'job_type',]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RemoteJobCreate, self).dispatch(*args, **kwargs)


    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(RemoteJobCreate, self).get_initial()

        # don't damage the original dict
        initial = initial.copy()
        initial['study'] = self.request.GET.get("study")
        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(commit=False)
        obj.created_by = self.request.user

        job_type = int(self.request.POST.get("job_type", 0))
        if job_type == 1:
            # a Remote query
            rq = RemoteQuery()
            rq.host = self.request.POST.get("remote_query_host", "")
            rq.query = self.request.POST.get("remote_query_query", "")
            rq.username = self.request.POST.get("remote_query_username", "")
            rq.password = self.request.POST.get("remote_query_password", "")
            rq.params = "{}"
            rq.created_by = self.request.user
            rq.celery_job = rq.queue_job()
            rq.save()
            obj.job_id = rq.id

        obj.save()
        return super(RemoteJobCreate, self).form_valid(form)

class RemoteJobUpdate(UpdateView):
    form_class = RemoteJobForm
    template_name = 'remote_jobs/remote_job_add.html'
    model = RemoteJob

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RemoteJobUpdate, self).dispatch(*args, **kwargs)


class RemoteJobDelete(DeleteView):
    model = RemoteJob
    template_name = 'remote_jobs/remote_job_confirm_delete.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        rj = RemoteJob.objects.get(pk=self.kwargs.get('pk'))
        self.success_url = reverse_lazy('study_detail', kwargs={'pk': rj.study.id, })
        return super(RemoteJobDelete, self).dispatch(*args, **kwargs)
