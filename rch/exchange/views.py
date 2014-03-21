from django.shortcuts import render
from django.views.generic.edit import FormView
from exchange.forms import OperationForm


class DepositView(FormView):

    template_name = 'operation.html'
    form_class = OperationForm
    success_url = '/thanks/'

    def form_valid(self, form):
        #TODO send command
        return super(DepositView, self).form_valid(form)



