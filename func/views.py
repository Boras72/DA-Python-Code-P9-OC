from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
#from .models import Ticket, Review, UserFollows


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST,request.FILES)
        if form.is_valid():
            ticket = form.save()
            ticket.user = request.user
            ticket.save()
           
    return render(request,create_ticket.html,
    context={'form':form}) 
    
    
@login_required
def edit_ticket(request, ticket_id):
    # Initialisation du formulaire 
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST,request.FILES)
        if form.is_valid():
            ticket = form.save()
            ticket.user = request.user
            ticket.save()
           
    return render(request,edit_ticket.html,
    context={'form':form}) 



