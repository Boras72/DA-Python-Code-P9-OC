from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows




@login_required(login_url='login')
def feed(request):
    # Récupérer les tickets et critiques des utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(user__in=followed_users)
    reviews = Review.objects.filter(user__in=followed_users)

    # Inclure les propres tickets et critiques de l'utilisateur
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    # Avis en réponse aux tickets de l'utilisateur connecté
    response_reviews = Review.objects.filter(ticket__in=user_tickets)

    # Combiner les queryset
    all_posts = sorted(
        list(tickets) + list(reviews) + list(user_tickets) + list(user_reviews) + list(response_reviews), #
        key=lambda x: x.time_created,
        reverse=True
    )

    context = {'posts': all_posts}
    return render(request, 'feed.html', context)


# Créer un Ticket
@login_required(login_url='login')
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()
    return render(request, 'ticket_create.html', {'form': form}) # S'assurer que les chemins des templates soient corrects dans les vues

# Modifier un Ticket   
@login_required(login_url='login')
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('feed')
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'ticket_edit.html', {'form': form})


# Supprimer un Ticket
@login_required(login_url='login')
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('feed')
    if request.method == 'POST':
        ticket.delete()
        return redirect('feed')
    return render(request, 'ticket_delete.html', {'ticket': ticket})




#### Créer une Critique en Réponse à un Ticket
@login_required(login_url='login')
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Vérifier que l'utilisateur suit l'auteur du ticket
    if not UserFollows.objects.filter(user=request.user, followed_user=ticket.user).exists():
        return redirect('feed')
    # Vérifier que l'utilisateur n'a pas déjà soumis une critique pour ce ticket
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect('feed')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'ticket': ticket})


#### Créer un Ticket et une Critique en Une Étape
@login_required(login_url='login')
def create_ticket_review(request):   
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'create_ticket_review.html', {'ticket_form': ticket_form, 'review_form': review_form})


# Modifier une Critique
@login_required(login_url='login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('feed')
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})



# Supprimer une Critique
@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('feed')
    if request.method == 'POST':
        review.delete()
        return redirect('feed')
    return render(request, 'delete_review.html', {'review': review})


