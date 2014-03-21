from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import FormView
from exchange.forms import OperationForm


def home(request):
    return render(request,'index.html')

class DepositView(FormView):

    template_name = 'operation.html'
    form_class = OperationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #TODO send command
        return super(DepositView, self).form_valid(form)



