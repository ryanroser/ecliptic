from django.views.generic.edit import CreateView
from django.views.generic import FormView, View

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User


class AccountCreate(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('study_list')


class AccountLogin(FormView):
    form_class = AuthenticationForm
    template_name = 'auth/user_form.html'

    def form_valid(self, form):
        redirect_to = reverse_lazy('study_list')
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)

    def form_invalid(self, form):
        print "INVALID"
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(AccountLogin, self).dispatch(request, *args, **kwargs)

class AccountLogout(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy('account_login'))
