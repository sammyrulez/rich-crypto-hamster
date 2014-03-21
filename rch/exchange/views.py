from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import FormView
from exchange.forms import OperationForm
from event_sourcing import command_executed


def home(request):
    return render(request,'index.html')

class DepositView(FormView):

    template_name = 'operation.html'
    form_class = OperationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #send(sender=self, toppings=toppings, size=size)
        command_executed.send(self,command_name="deposit",payload=form.cleaned_data)
        return super(DepositView, self).form_valid(form)



