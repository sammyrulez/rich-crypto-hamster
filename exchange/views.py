from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import FormView
from exchange.forms import OperationForm
from event_sourcing import command_executed


def home(request):
    return render(request, 'index.html')


class OperationView(FormView):
    template_name = 'operation.html'
    form_class = OperationForm
    success_url = reverse_lazy('home')
    command_name = None

    def form_valid(self, form):
        command_executed.send(self, command=self.command_name, payload=form.cleaned_data)
        return super(OperationView, self).form_valid(form)


class DepositView(OperationView):
    command_name = 'deposit'


class WithdrawView(OperationView):
    command_name = 'withdraw'
