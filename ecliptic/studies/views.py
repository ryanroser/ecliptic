from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from studies.models import Study
from studies.forms import StudyForm

from studies.tasks import add

class StudyList(ListView):
    model = Study

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudyList, self).dispatch(*args, **kwargs)

class StudyDetail(DetailView):
    model = Study

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudyDetail, self).dispatch(*args, **kwargs)

class StudyCreate(CreateView):
    form_class = StudyForm
    template_name = 'studies/study_add.html'
    model = Study
    fields = ['name', 'hypothesis',]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudyCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return super(StudyCreate, self).form_valid(form)

class StudyUpdate(UpdateView):
    form_class = StudyForm
    template_name = 'studies/study_add.html'
    model = Study
    #fields = ['name']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudyUpdate, self).dispatch(*args, **kwargs)

class StudyDelete(DeleteView):
    model = Study
    success_url = reverse_lazy('study_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudyDelete, self).dispatch(*args, **kwargs)
